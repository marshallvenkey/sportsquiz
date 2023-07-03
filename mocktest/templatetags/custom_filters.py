from django import template
from datetime import timedelta

register = template.Library()

@register.filter
def get_value(dictionary, key):
    return dictionary.get(key, '')


@register.filter
def calculate_test_time(test_result):
    duration = test_result.end_time - test_result.start_time
    minutes = duration.total_seconds() // 60
    seconds = duration.total_seconds() % 60
    return f"{int(minutes)} minutes, {int(seconds)} seconds"