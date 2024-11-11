from django import template
from decimal import Decimal

register = template.Library()

@register.filter
def increase_by_20_percent(value):
    return int(value * Decimal('1.2'))