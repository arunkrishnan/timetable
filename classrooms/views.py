from rest_framework.viewsets import ModelViewSet

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


class TeacherViewSet(ModelViewSet):
    queryset = Teacher.objects.all()  # Filter by school, based on logged in user
    serializer_class = TeacherSerializer


class SubjectViewSet(ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class SubjectTeacherViewSet(ModelViewSet):
    queryset = SubjectTeacher.objects.all()
    serializer_class = SubjectTeacherSerializer


class PeriodViewSet(ModelViewSet):
    queryset = Period.objects.all()
    serializer_class = PeriodSerializer
