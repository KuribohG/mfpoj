# -*- coding: utf-8 -*-
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(is_safe=True)
@stringfilter

def displaymarkdowncode(value):
    return "```" + value + "```"
