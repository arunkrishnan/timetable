from django.db import models
from django.utils import timezone

from utils.model_manager_templates import LogicalDeletedManager, get_related_objects


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    @classmethod
    def from_db(cls, db, field_names, values):
        instance = super(BaseModel, cls).from_db(db, field_names, values)
        instance._loaded_values = dict(zip(field_names, values))
        return instance


class LogicalDeleteModel(BaseModel):
    """
    This base model provides date fields and functionality to enable logical
    delete functionality in derived models.
    """

    date_removed = models.DateTimeField(null=True, blank=True)

    objects = LogicalDeletedManager()

    def active(self):
        return self.date_removed is None

    active.boolean = True

    def delete(self, *args, **kwargs):
        # Fetch related models
        to_delete = get_related_objects(self)
        for obj in to_delete:
            obj.delete()
        # Soft delete the object
        self.date_removed = timezone.now()
        self.save()

    class Meta:
        abstract = True
