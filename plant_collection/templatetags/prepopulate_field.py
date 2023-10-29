from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

#Does not work
@register.filter
@stringfilter
def prepopulate_input(value, insert):
    at= value.find('>')
    return value[0:at] + ' name=' + "'" +insert + "'" + ">"
