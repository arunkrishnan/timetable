from datetime import datetime

from django.core.exceptions import ValidationError
from django_filters import rest_framework as filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.viewsets import ModelViewSet

from classrooms.helpers import (
    available_teachers_for_the_period,
    get_period_adjustment_insights,
)
from classrooms.models import (
    Period,
    SubjectTeacher,
    ClassRoom,
    Subject,
    PeriodAdjustment,
)
from classrooms.serializers import (
    PeriodSerializer,
    SubjectTeacherSerializer,
    ClassRoomSerializer,
    SubjectSerializer,
    PeriodAdjustmentSerializer,
)
from schools.models import Teacher
from utils.futils import get_current_admission_year


class ClassRoomViewSet(ModelViewSet):
    queryset = ClassRoom.objects.all()
    serializer_class = ClassRoomSerializer

    def get_queryset(self):
        return self.queryset.filter(school=self.request.school)


class SubjectViewSet(ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class SubjectTeacherViewSet(ModelViewSet):
    queryset = SubjectTeacher.objects.all()
    serializer_class = SubjectTeacherSerializer

    def get_queryset(self):
        return self.queryset.filter(teacher__school=self.request.school)


class PeriodFilter(filters.FilterSet):
    teacher = filters.CharFilter(field_name="subject_teacher__teacher")
    date = filters.CharFilter(method="filter_by_date")

    class Meta:
        model = Period
        fields = ["weekday", "admission_year", "teacher", "classroom"]

    def filter_by_date(self, queryset, name, value):
        day = datetime.strptime(value, "%Y-%m-%d").isoweekday() % 7
        queryset = queryset.filter(weekday=day)
        period_adjustments = PeriodAdjustment.objects.filter(
            adjusted_date=value, period__in=queryset
        )
        if not period_adjustments:
            return queryset

        adjusted_periods = [adjustment.period for adjustment in period_adjustments]
        for period in queryset:
            if period in adjusted_periods:
                period.subject_teacher = PeriodAdjustment.objects.get(
                    adjusted_date=value, period=period
                ).adjusted_by
        return queryset


class PeriodViewSet(ModelViewSet):
    queryset = Period.objects.filter(
        admission_year=get_current_admission_year()
    ).order_by("-id")
    serializer_class = PeriodSerializer
    filterset_class = PeriodFilter

    def get_queryset(self):
        return self.queryset.filter(classroom__school=self.request.school)

    @action(
        detail=True,
        url_path="free-teachers",
        methods=["get"],
        serializer_class=SubjectTeacherSerializer,
    )
    def get_available_teachers(self, request, pk=None):
        period = self.get_object()
        try:
            date = request.query_params["date"]
            date_obj = datetime.strptime(date, "%Y-%m-%d")
            weekday = date_obj.isoweekday() % 7
            if not weekday == period.weekday:
                return Response(
                    "Date and period object doesn't match", HTTP_400_BAD_REQUEST
                )
        except KeyError:
            return Response("Date is missing in the request", HTTP_400_BAD_REQUEST)
        teachers = available_teachers_for_the_period(period, date_obj)
        page = self.paginate_queryset(teachers)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(teachers, many=True)
        return Response(serializer.data)

    @action(detail=True, url_path="insights", methods=["get"])
    def get_insights(self, request, pk=None):
        period = self.get_object()
        try:
            subject_teacher_id = request.query_params[
                "subject_teacher_id"
            ]  # The teacher who going to replace the period
            date = request.query_params["date"]
        except KeyError:
            return Response(
                "Subject teacher id / date is missing in the request",
                HTTP_400_BAD_REQUEST,
            )
        try:
            teacher = SubjectTeacher.objects.get(id=subject_teacher_id)
        except (ValidationError, Teacher.DoesNotExist):
            return Response("Wrong Subject Teacher id in the request", HTTP_400_BAD_REQUEST)

        insights = get_period_adjustment_insights(period, teacher, date)

        return Response(insights, status=200)


class PeriodAdjustmentFilter(filters.FilterSet):
    date = filters.CharFilter(field_name="adjusted_date")

    class Meta:
        model = PeriodAdjustment
        fields = ["date"]


class PeriodAdjustmentViewSet(ModelViewSet):
    queryset = PeriodAdjustment.objects.all().order_by("-id")
    serializer_class = PeriodAdjustmentSerializer
    filterset_class = PeriodAdjustmentFilter

    def get_queryset(self):
        return self.queryset.filter(period__classroom__school=self.request.school)