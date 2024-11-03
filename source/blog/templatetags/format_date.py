from django import template
from bs4 import BeautifulSoup
import hashlib

register = template.Library()

MONTHS_RU = {
    1: 'января', 2: 'февраля', 3: 'марта', 4: 'апреля',
    5: 'мая', 6: 'июня', 7: 'июля', 8: 'августа',
    9: 'сентября', 10: 'октября', 11: 'ноября', 12: 'декабря'
}

MONTHS_EN = {
    1: 'January', 2: 'February', 3: 'March', 4: 'April',
    5: 'May', 6: 'June', 7: 'July', 8: 'August',
    9: 'September', 10: 'October', 11: 'November', 12: 'December'
}


@register.filter
def format_date(date, lang='ru'):
    day = date.day
    month = date.month
    year = date.year

    if lang == 'en':
        month_name = MONTHS_EN.get(month, '')
    else:
        month_name = MONTHS_RU.get(month, '')

    return f"{day} {month_name} {year}"
