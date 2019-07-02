from django.utils.deprecation import MiddlewareMixin

from schools.models import School


class CmsLogin(MiddlewareMixin):
    def process_request(self, request):
        school = School.objects.get(id=1)
        request.school = school
