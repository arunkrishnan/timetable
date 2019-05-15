from django.core.exceptions import ValidationError

from classrooms.factories import (
    PeriodFactory,
    SubjectTeacherFactory,
    ClassRoomFactory,
)

import pytest

from schools.factories import SchoolFactory, TeacherFactory


@pytest.mark.django_db
def test_period_model():
    # A teacher can not have 2 periods simultaneously

    school = SchoolFactory()
    teacher = TeacherFactory(school=school)
    cr1 = ClassRoomFactory(school=school)
    cr2 = ClassRoomFactory(school=school)
    subject_1 = SubjectTeacherFactory(teacher=teacher)
    subject_2 = SubjectTeacherFactory(teacher=teacher)

    PeriodFactory(weekday=1, period_number=1, subject_teacher=subject_1, classroom=cr1)

    with pytest.raises(ValidationError):
        PeriodFactory(
            subject_teacher=subject_2, weekday=1, period_number=1, classroom=cr2
        )


@pytest.mark.django_db
def test_school_validation():
    school1 = SchoolFactory()
    school2 = SchoolFactory()
    teacher = TeacherFactory(school=school1)
    classroom = ClassRoomFactory(school=school2)
    subject_teacher = SubjectTeacherFactory(teacher=teacher)
    with pytest.raises(ValidationError):
        PeriodFactory(
            weekday=1,
            period_number=1,
            subject_teacher=subject_teacher,
            classroom=classroom,
        )
