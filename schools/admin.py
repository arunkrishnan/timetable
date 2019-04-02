from django.contrib import admin

from schools.models import School


class SchoolAdmin(admin.ModelAdmin):
    model = School
    list_display = ("name", "code")
    list_filter = ("name", "code")
    search_fields = ("name", "code")
    ordering = ("code", "name")


admin.site.register(School, SchoolAdmin)
