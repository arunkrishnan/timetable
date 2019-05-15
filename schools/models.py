import uuid
from uuid import uuid4

from django.db import models
from django.db.models import UUIDField

from utils.model_templates import LogicalDeleteModel


class School(LogicalDeleteModel):
    id = UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=5, unique=True)

    def __str__(self):
        return f"{self.code}-{self.name}"


class Teacher(LogicalDeleteModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=100, null=True, blank=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=150, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name
