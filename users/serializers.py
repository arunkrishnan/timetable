from rest_framework import serializers

from users.models import CustomUser


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("url", "email", "is_staff", "first_name", "last_name")
