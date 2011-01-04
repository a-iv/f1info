# -*- coding: utf-8 -*-

from django import template
from f1info.models import GrandPrix, Heat, Season, GPName, Racer
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

@register.inclusion_tag('f1info/tags/standings.html', takes_context=False)
def show_standings():
    results = Season.objects.get(year=2010)
    return {'object': results}

@register.inclusion_tag('f1info/tags/calendar.html', takes_context=False)
def show_calendar():
    current = datetime.datetime.today()
    gp = GrandPrix.objects.filter(season=Season.objects.get(year=2010))
    return {'objects': gp, 'current': current, }

@register.inclusion_tag('f1info/tags/winners.html', takes_context=False)
def show_winners(gpid):
    gpname = GPName.objects.get(id=gpid)
    gp = GrandPrix.objects.filter(name=gpname)
    return {'objects': gp, }

@register.inclusion_tag('f1info/tags/today.html', takes_context=False)
def show_today():
    today = datetime.datetime.today()
    racers = Racer.objects.filter(birthday__day=today.day, birthday__month=today.month)
    return {'racers': racers, 'today': today, }
