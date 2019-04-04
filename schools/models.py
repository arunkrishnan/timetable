from uuid import uuid4

from django.db import models
from django.db.models import UUIDField

from utils.model_templates import LogicalDeleteModel


class School(LogicalDeleteModel):
    id = UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=7, unique=True)

    def __str__(self):
        return f"{self.code}-{self.name}"
