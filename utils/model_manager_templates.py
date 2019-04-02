import itertools

from django.contrib.admin.utils import NestedObjects
from django.db import models, DEFAULT_DB_ALIAS

from utils.model_query_templates import LogicalDeleteQuerySet


class LogicalDeletedManager(models.Manager):
    """
    A manager that serves as the default manager for `pinax.models.LogicalDeleteModel`
    providing the filtering out of logically deleted objects. In addition, it
    provides named querysets for getting the deleted objects.
    """

    def get_queryset(self):
        if self.model:
            return LogicalDeleteQuerySet(self.model, using=self._db).filter(
                date_removed__isnull=True
            )

    def all_with_deleted(self):
        if self.model:
            return super(LogicalDeletedManager, self).get_queryset()

    def only_deleted(self):
        if self.model:
            return (
                super(LogicalDeletedManager, self)
                .get_queryset()
                .filter(date_removed__isnull=False)
            )

    def get(self, *args, **kwargs):
        if "pk" in kwargs:
            return self.all_with_deleted().get(*args, **kwargs)
        return self.get_queryset().get(*args, **kwargs)

    def filter(self, *args, **kwargs):
        if "pk" in kwargs:
            return self.all_with_deleted().filter(*args, **kwargs)
        return self.get_queryset().filter(*args, **kwargs)


def get_related_objects(obj, using=DEFAULT_DB_ALIAS):
    # This code is based on https://github.com/makinacorpus/django-safedelete
    collector = NestedObjects(using=using)
    collector.collect([obj])

    def flatten(elem):
        if isinstance(elem, list):
            return itertools.chain.from_iterable(map(flatten, elem))
        elif obj != elem:
            return (elem,)
        return ()

    return flatten(collector.nested())
