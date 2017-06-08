# create template filter
from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter(name='times')
@stringfilter
def times(number):
    return range(int(number))
