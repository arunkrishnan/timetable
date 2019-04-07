from typing import List, Set

from classrooms.models import Teacher, Period, ClassRoom, SubjectTeacher


def get_teachers_of_class(classroom: ClassRoom, admission_year: int) -> Set[Teacher]:
    periods = Period.objects.filter(classroom=classroom, admission_year=admission_year)
    teachers = {period.subject_teacher.teacher for period in periods}
    return teachers


def available_teachers(
    teachers: Set[Teacher], weekday: int, period_number: int, admission_year: int
) -> List[Teacher]:
    free_teachers = []
    for teacher in teachers:
        subject_teachers = SubjectTeacher.objects.filter(teacher=teacher)
        if not Period.objects.filter(
            admission_year=admission_year,
            weekday=weekday,
            period_number=period_number,
            subject_teacher__in=subject_teachers,
        ).exists():
            free_teachers.append(teacher)
    return free_teachers


def available_teachers_for_the_period(period: Period) -> List[Teacher]:
    admission_year = period.admission_year
    class_teachers = get_teachers_of_class(period.classroom, admission_year)
    teachers = available_teachers(
        class_teachers, period.weekday, period.period_number, admission_year
    )
    return teachers
