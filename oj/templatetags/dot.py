# -*- coding: utf-8 -*-
import json

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(is_safe=True)
@stringfilter
def dot(stat,score):
    obj = json.loads(stat)
    if score in stat:
        return obj[score]
    else:
        return -1
