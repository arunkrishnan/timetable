from django.contrib import admin

from classrooms.models import (
    ClassRoom,
    Teacher,
    Subject,
    SubjectTeacher,
    Period,
    PeriodAdjustment,
)


class ClassRoomAdmin(admin.ModelAdmin):
    model = ClassRoom
    list_display = ("standard", "division", "school")
    list_filter = ("standard", "division", "school")
    search_fields = ("standard", "division", "school")
    ordering = ("standard", "division", "school")


class TeacherAdmin(admin.ModelAdmin):
    model = Teacher
    list_display = ("code", "school", "first_name", "email")
    list_filter = ("code", "school", "first_name", "email")
    search_fields = ("code", "school", "first_name", "email")
    ordering = ("code", "school", "first_name", "email")


class SubjectAdmin(admin.ModelAdmin):
    model = Subject
    list_display = ("name", "code")
    list_filter = ("name", "code")
    search_fields = ("name", "code")
    ordering = ("code", "name")


class SubjectTeacherAdmin(admin.ModelAdmin):
    model = SubjectTeacher
    list_display = ("subject", "teacher")
    list_filter = ("subject", "teacher")
    search_fields = ("subject", "teacher")
    ordering = ("subject", "teacher")


class PeriodAdmin(admin.ModelAdmin):
    model = Period
    list_display = (
        "classroom",
        "weekday",
        "period_number",
        "subject_teacher",
        "admission_year",
    )
    list_filter = ("classroom", "weekday", "period_number", "subject_teacher", "admission_year")
    search_fields = (
        "classroom",
        "weekday",
        "period_number",
        "subject_teacher",
        "admission_year",
    )
    ordering = ("classroom", "weekday", "period_number", "subject_teacher", "admission_year")


class PeriodAdjustmentAdmin(admin.ModelAdmin):
    model = PeriodAdjustment
    list_display = ("adjusted_date", "period", "adjusted_by")
    list_filter = ("adjusted_date", "period", "adjusted_by")
    search_fields = ("adjusted_date", "period", "adjusted_by")
    ordering = ("adjusted_date", "period", "adjusted_by")


admin.site.register(ClassRoom, ClassRoomAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(SubjectTeacher, SubjectTeacherAdmin)
admin.site.register(Period, PeriodAdmin)
admin.site.register(PeriodAdjustment, PeriodAdjustmentAdmin)
