from django.utils.deprecation import MiddlewareMixin

from schools.models import School


class CmsLogin(MiddlewareMixin):
    def process_request(self, request):
        school = School.objects.all()[0]
        request.school = school
