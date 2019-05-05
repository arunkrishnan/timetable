from django.core.exceptions import ValidationError

from classrooms.factories import PeriodFactory, TeacherFactory, SubjectTeacherFactory

import pytest


@pytest.mark.django_db
def test_period_model():
    # A teacher can not have 2 periods simultaneously

    teacher = TeacherFactory()
    subject_1 = SubjectTeacherFactory(teacher=teacher)
    subject_2 = SubjectTeacherFactory(teacher=teacher)

    PeriodFactory(weekday=1, period_number=1, subject_teacher=subject_1)

    with pytest.raises(ValidationError):
        PeriodFactory(subject_teacher=subject_2, weekday=1, period_number=1)
