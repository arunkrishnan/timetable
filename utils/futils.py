from django.utils import timezone


def get_current_admission_year():
    today = timezone.now()
    if today.month < 5:
        return today.year
    return today.year + 1
