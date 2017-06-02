import json

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(is_safe=True)

def quotient(a,b):
    if b == 0:
        return "0.00"
    else:
        return str("%.2f" % (a*100.00/b))




