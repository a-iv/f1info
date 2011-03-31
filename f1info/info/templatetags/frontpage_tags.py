# -*- coding: utf-8 -*-

from django import template
from f1info.models import *
from pages.models import *
import datetime

register = template.Library()

@register.inclusion_tag('f1info/tags/nextgp.html', takes_context=False)
def show_nextgp():
    current = datetime.datetime.today()
    try:
        next = Heat.objects.filter(date__gte=current)[:1]
        gp = GrandPrix.objects.filter(heats=next)
        start = Heat.objects.filter(grandprix=gp)[0]
        end = get_last(Heat.objects.filter(grandprix=gp))
        return {'nextgp': next, 'current': current, 'start': start, 'end': end,}
    except:
        pass

@register.inclusion_tag('f1info/tags/standings.html', takes_context=False)
def show_standings():
    results = Season.objects.get(year=2011)
    return {'object': results}

@register.inclusion_tag('f1info/tags/calendar.html', takes_context=False)
def show_calendar(year):
    this_year = datetime.datetime.today()
    gp = GrandPrix.objects.filter(season=Season.objects.get(year=str(year)))
    return {'objects': gp, }

@register.inclusion_tag('f1info/tags/winners.html', takes_context=False)
def show_winners(gpid):
    gpname = GPName.objects.get(id=gpid)
    gp = GrandPrix.objects.filter(name=gpname)
    return {'objects': gp, }

@register.inclusion_tag('f1info/tags/today.html', takes_context=False)
def show_today():
    today = datetime.datetime.today()
    racers = Racer.objects.filter(birthday__day=today.day, birthday__month=today.month)
    heats = Heat.objects.filter(type='R', date__day=today.day, date__month=today.month)
    return {'racers': racers, 'heats': heats, 'today': today, }

@register.inclusion_tag('f1info/tags/twitters.html', takes_context=False)
def show_twitter():
    twitters = Racer.objects.exclude(twitter=None)
    return {'twitters': twitters, }

@register.inclusion_tag('f1info/tags/current_letter.html', takes_context=False)
def show_current_letter(letter):
    first_letter = str(letter)[0]
    letters = Racer.objects.filter(family_name__startswith=first_letter)
    return {'letters': letters, }

@register.inclusion_tag('f1info/tags/onthisday.html', takes_context=False)
def show_onthisday():
    current = datetime.datetime.today().strftime("%d.%m")
    for page in Page.objects.all():
        template = page.get_template()
        if template == 'pages/onthisday.html':
            day_field = Content.objects.get_content(page, None, "day")
            if day_field == current:
               return {'page': page, }

