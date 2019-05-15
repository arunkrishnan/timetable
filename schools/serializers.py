from rest_framework import serializers

from schools.models import Teacher


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        read_only_fields = ("full_name",)
        fields = ("id", "full_name", "code")
