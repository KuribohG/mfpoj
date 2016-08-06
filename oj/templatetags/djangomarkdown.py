# -*- coding: utf-8 -*-

import markdown2

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(is_safe=True)
@stringfilter
def djangomarkdown(value):
    return mark_safe(markdown2.markdown(value, extras=["code-friendly"]))
