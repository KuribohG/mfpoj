# -*- coding: utf-8 -*-

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(is_safe=True)
@stringfilter
def num2letter(value):
    return mark_safe(chr(ord('A') + int(value) - 1))
