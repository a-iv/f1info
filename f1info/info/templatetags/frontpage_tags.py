# -*- coding: utf-8 -*-

from django import template
from f1info.models import GrandPrix, Heat
import datetime

register = template.Library()

@register.inclusion_tag('f1info/tags/nextgp.html', takes_context=False)
def show_nextgp():
    current = datetime.datetime.today()
    try:
        next = Heat.objects.filter(date__gte=current)[:1]
        gp = GrandPrix.objects.filter(heats=next)
        start = Heat.objects.filter(grandprix=gp)[0]
        end = Heat.objects.filter(grandprix=gp).latest('date')
        return {'nextgp': next, 'current': current, 'start': start, 'end': end,}
    except:
        pass
