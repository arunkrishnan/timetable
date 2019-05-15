from random import randint, choice

import factory

from classrooms.models import ClassRoom, Subject, SubjectTeacher, Period
from schools.factories import SchoolFactory, TeacherFactory


class ClassRoomFactory(factory.DjangoModelFactory):
    class Meta:
        model = ClassRoom

    standard = factory.LazyAttribute(lambda n: str(randint(1, 10)))
    division = factory.LazyAttribute(lambda n: choice(["A", "B", "C", "D", "E"]))
    school = factory.SubFactory(SchoolFactory)


class SubjectFactory(factory.DjangoModelFactory):
    class Meta:
        model = Subject

    name = factory.Faker("catch_phrase")
    code = factory.LazyAttribute(lambda obj: obj.name[:5])


class SubjectTeacherFactory(factory.DjangoModelFactory):
    class Meta:
        model = SubjectTeacher

    teacher = factory.SubFactory(TeacherFactory)
    subject = factory.SubFactory(SubjectFactory)


class PeriodFactory(factory.DjangoModelFactory):
    class Meta:
        model = Period

    classroom = factory.SubFactory(ClassRoomFactory)
    weekday = factory.LazyAttribute(lambda n: str(randint(1, 7)))
    period_number = factory.LazyAttribute(lambda n: str(randint(1, 7)))
    subject_teacher = factory.SubFactory(SubjectTeacherFactory)
