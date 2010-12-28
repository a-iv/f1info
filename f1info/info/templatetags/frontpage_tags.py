# -*- coding: utf-8 -*-

from django import template
from f1info.models import Heat
import datetime

register = template.Library()

@register.inclusion_tag('f1info/tags/nextgp.html', takes_context=False)
def show_nextgp():
    next = Heat.objects.all()
    current = datetime.datetime.today()
    return {'nextgp': next, 'current': current,}
