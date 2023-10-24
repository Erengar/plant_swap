from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

#Does not work
@register.filter
@stringfilter
def error(value):
    if 'class' in value:
        at= value.find('class')
        return value[0:at+7] + "is-danger " + value[10:]
    at = value.find('>')
    return value[0:at] +" class='is-danger'"+ value[at:]
