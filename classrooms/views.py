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
from classrooms.models import Period, SubjectTeacher, ClassRoom, Teacher, Subject
from classrooms.serializers import (
    PeriodSerializer,
    SubjectTeacherSerializer,
    ClassRoomSerializer,
    TeacherSerializer,
    SubjectSerializer,
)


class ClassRoomViewSet(ModelViewSet):
    queryset = ClassRoom.objects.all()
    serializer_class = ClassRoomSerializer


class TeacherFilter(filters.FilterSet):
    class Meta:
        model = Teacher
        fields = {
            "id": ["exact"],
            "code": ["exact"],
            "school": ["exact"],
            "first_name": ["exact", "contains"],
            "email": ["exact"],
            "phone_number": ["exact"],
            "school__code": ["exact"],
        }


class TeacherViewSet(ModelViewSet):
    queryset = Teacher.objects.all()  # Filter by school, based on logged in user
    serializer_class = TeacherSerializer
    filterset_class = TeacherFilter


class SubjectViewSet(ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class SubjectTeacherViewSet(ModelViewSet):
    queryset = SubjectTeacher.objects.all()
    serializer_class = SubjectTeacherSerializer


class PeriodFilter(filters.FilterSet):
    teacher = filters.CharFilter(field_name="subject_teacher__teacher")

    class Meta:
        model = Period
        fields = ["weekday", "admission_year", "teacher", "classroom"]


class PeriodViewSet(ModelViewSet):
    queryset = Period.objects.all()
    serializer_class = PeriodSerializer
    filterset_class = PeriodFilter

    @action(
        detail=True,
        url_path="free-teachers",
        methods=["get"],
        serializer_class=TeacherSerializer,
    )
    def get_available_teachers(self, request, pk=None):
        period = self.get_object()
        teachers = available_teachers_for_the_period(period)
        page = self.paginate_queryset(teachers)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(teachers, many=True)
        return Response(serializer.data)

    @action(detail=True, url_path="insights", methods=["get"])
    def get_insights(self, request, pk=None):
        period = self.get_object()
        teacher_id = request.GET.get("teacher_id")
        if not teacher_id:
            return Response(
                "Teacher id is missing in the request", HTTP_400_BAD_REQUEST
            )
        try:
            teacher = Teacher.objects.get(id=teacher_id)
        except (ValidationError, Teacher.DoesNotExist):
            return Response("Wrong Teacher id in the request", HTTP_400_BAD_REQUEST)

        insights = get_period_adjustment_insights(period, teacher)

        return Response(insights, status=200)
