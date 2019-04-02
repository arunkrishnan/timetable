import factory

from schools.models import School


class SchoolFactory(factory.DjangoModelFactory):
    class Meta:
        model = School

    name = factory.Faker("name")
    code = factory.LazyAttribute(lambda obj: obj.name[:4])
