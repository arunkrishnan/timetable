from typing import List, Set, Dict

from classrooms.models import Teacher, Period, ClassRoom, SubjectTeacher


def get_teachers_of_class(classroom: ClassRoom, admission_year: int) -> Set[Teacher]:
    periods = Period.objects.filter(classroom=classroom, admission_year=admission_year)
    teachers = {period.subject_teacher.teacher for period in periods}
    return teachers


def available_teachers(
    teachers: Set[Teacher], weekday: int, period_number: int, admission_year: int
) -> List[SubjectTeacher]:
    free_teachers = []
    for teacher in teachers:
        subject_teachers = SubjectTeacher.objects.filter(teacher=teacher)
        if not Period.objects.filter(
            admission_year=admission_year,
            weekday=weekday,
            period_number=period_number,
            subject_teacher__in=subject_teachers,
        ).exists():
            free_teachers.append(subject_teachers[0])
    return free_teachers


def available_teachers_for_the_period(period: Period) -> List[SubjectTeacher]:
    admission_year = period.admission_year
    class_teachers = get_teachers_of_class(period.classroom, admission_year)
    teachers = available_teachers(
        class_teachers, period.weekday, period.period_number, admission_year
    )
    return teachers


def get_period_adjustment_insights(period: Period, teacher: Teacher) -> Dict:
    insights = {}
    classroom = period.classroom
    weekday = period.weekday
    period_number = period.period_number
    admission_year = period.admission_year

    subject_teachers = SubjectTeacher.objects.filter(teacher=teacher)
    insights["total_periods_allotted"] = Period.objects.filter(
        weekday=weekday,
        admission_year=admission_year,
        subject_teacher__in=subject_teachers,
    ).count()

    insights["periods_in_the_same_class"] = Period.objects.filter(
        weekday=weekday,
        classroom=classroom,
        admission_year=admission_year,
        subject_teacher__in=subject_teachers,
    ).count()
    insights["had_class_in_previous_period"] = Period.objects.filter(
        weekday=weekday,
        period_number=period_number - 1,
        admission_year=admission_year,
        subject_teacher__in=subject_teachers,
    ).exists()
    insights["have_class_in_next_period"] = Period.objects.filter(
        weekday=weekday,
        period_number=period_number - 1,
        admission_year=admission_year,
        subject_teacher__in=subject_teachers,
    ).exists()

    return insights
