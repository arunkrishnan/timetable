from random import randint, choice

import factory

from classrooms.models import ClassRoom, Teacher, Subject, SubjectTeacher, Period
from schools.factories import SchoolFactory


class ClassRoomFactory(factory.DjangoModelFactory):
    class Meta:
        model = ClassRoom

    standard = factory.LazyAttribute(lambda n: str(randint(1, 10)))
    division = factory.LazyAttribute(lambda n: choice(["A", "B", "C", "D", "E"]))
    school = factory.SubFactory(SchoolFactory)


class TeacherFactory(factory.DjangoModelFactory):
    class Meta:
        model = Teacher

    teacher_code = factory.Faker("user_name")
    school = factory.SubFactory(SchoolFactory)
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    phone_number = factory.LazyAttribute(lambda n: str(randint(11111, 55555)))


class SubjectFactory(factory.DjangoModelFactory):
    class Meta:
        model = Subject

    name = factory.Faker("catch_phrase")
    code = factory.LazyAttribute(lambda obj: obj.name[:5])


class SubjectTeacherFactory(factory.DjangoModelFactory):
    class Meta:
        model = SubjectTeacher

    teacher = factory.SubFactory(TeacherFactory)
    subject = factory.SubFactory(SubjectTeacher)


class PeriodFactory(factory.DjangoModelFactory):
    class Meta:
        model = Period

    classroom = factory.SubFactory(ClassRoomFactory)
    weekday = factory.LazyAttribute(lambda n: str(randint(1, 7)))
    period_number = factory.LazyAttribute(lambda n: str(randint(1, 7)))
    subject = factory.SubFactory(SubjectTeacher)
