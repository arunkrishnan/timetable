import uuid

from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from djchoices import DjangoChoices, ChoiceItem

from schools.models import School
from utils.futils import get_current_admission_year
from utils.model_templates import LogicalDeleteModel, BaseModel


class WeekDay(DjangoChoices):
    Sunday = ChoiceItem(0)
    Monday = ChoiceItem(1)
    Tuesday = ChoiceItem(2)
    Wednesday = ChoiceItem(3)
    Thursday = ChoiceItem(4)
    Friday = ChoiceItem(5)
    Saturday = ChoiceItem(6)


class ClassRoom(LogicalDeleteModel):
    standard = models.CharField(max_length=10)
    division = models.CharField(max_length=3)
    school = models.ForeignKey(School, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.standard} {self.division}"


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


class Subject(BaseModel):
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=4)

    def __str__(self):
        return self.name


class SubjectTeacher(BaseModel):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.subject.name}-{self.teacher.first_name}"


class Period(LogicalDeleteModel):
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    weekday = models.IntegerField(
        choices=WeekDay.choices, validators=[WeekDay.validator]
    )
    period_number = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(8)]
    )
    subject_teacher = models.ForeignKey(SubjectTeacher, on_delete=models.CASCADE)
    admission_year = models.IntegerField(default=get_current_admission_year)

    class Meta:
        unique_together = ("classroom", "weekday", "period_number", "admission_year")

    def clean(self, *args, **kwargs):
        teacher_id = self.subject_teacher.teacher
        subject_teachers = SubjectTeacher.objects.filter(teacher=teacher_id)
        if (
            Period.objects.filter(
                weekday=self.weekday,
                period_number=self.period_number,
                subject_teacher__in=subject_teachers,
                admission_year=self.admission_year,
            )
            .exclude(pk=self.pk)
            .exists()
        ):
            period = Period.objects.get(
                weekday=self.weekday,
                period_number=self.period_number,
                subject_teacher__in=subject_teachers,
                admission_year=self.admission_year,
            )
            raise ValidationError(f"Teacher already has a period {period.id}")

        super().clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class PeriodAdjustment(LogicalDeleteModel):
    adjusted_date = models.DateField()
    period = models.ForeignKey(Period, on_delete=models.CASCADE)
    adjusted_by = models.ForeignKey(SubjectTeacher, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("adjusted_date", "period")
