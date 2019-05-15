from random import randint

import factory

from schools.models import School, Teacher


class SchoolFactory(factory.DjangoModelFactory):
    class Meta:
        model = School

    name = factory.Faker("name")
    code = factory.LazyAttribute(lambda obj: obj.name[:4])


class TeacherFactory(factory.DjangoModelFactory):
    class Meta:
        model = Teacher

    code = factory.Faker("user_name")
    school = factory.SubFactory(SchoolFactory)
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    phone_number = factory.LazyAttribute(lambda n: str(randint(11111, 55555)))

