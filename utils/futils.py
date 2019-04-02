from django.utils import timezone


def get_current_year():
    today = timezone.now()
    return today.year
