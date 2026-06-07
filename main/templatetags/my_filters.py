from django import template

register = template.Library()

from django import template

register = template.Library()

@register.filter(name='persian_intcomma')
def persian_intcomma(value):
    try:
        num = int(float(value))
        # جداسازی سه رقم سه رقم با ویرگول
        result = '{:,}'.format(num)
        return result
    except (ValueError, TypeError):
        return value