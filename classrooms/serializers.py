from rest_framework import serializers

from classrooms.models import Period, SubjectTeacher, ClassRoom, Teacher, Subject


class ClassRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassRoom
        fields = ("id", "standard", "division")


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        read_only_fields = ("full_name",)
        fields = ("id", "full_name", "code")


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ("id", "name")


class SubjectTeacherSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer()
    teacher = TeacherSerializer()

    class Meta:
        model = SubjectTeacher
        fields = ("id", "subject", "teacher")


class PeriodSerializer(serializers.ModelSerializer):
    classroom = ClassRoomSerializer()
    subject_teacher = SubjectTeacherSerializer()

    class Meta:
        model = Period
        fields = ("id", "weekday", "classroom", "subject_teacher")
