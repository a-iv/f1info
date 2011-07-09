# -*- coding: utf-8 -*-

from django import template
from f1info.models import *
from pages.models import *
import datetime

register = template.Library()

@register.inclusion_tag('f1info/tags/nextgp.html', takes_context=False)
def show_nextgp():
    today = datetime.datetime.today()
    try:
        next = Heat.objects.filter(date__gte=today)[0]
        heats = next.grandprix.heats.exclude(type='B')
        return {'nextgp': next, 'heats': heats, }
    except:
        pass

@register.inclusion_tag('f1info/tags/standings.html', takes_context=False)
def show_standings():
    results = Season.objects.get(year=2011)
    return {'object': results}

@register.inclusion_tag('f1info/tags/today.html', takes_context=False)
def show_today():
    today = datetime.datetime.today()
    racers = Racer.objects.filter(birthday__day=today.day, birthday__month=today.month)
    heats = Heat.objects.filter(type='R', date__day=today.day, date__month=today.month)
    return {'racers': racers, 'heats': heats, 'today': today, }

@register.inclusion_tag('f1info/tags/twitters.html', takes_context=False)
def show_twitter():
    objects = Racer.objects.exclude(twitter='')
    return { 'objects': objects, }

@register.inclusion_tag('f1info/tags/current_letter.html', takes_context=False)
def show_current_letter(racer):
    letters = Racer.objects.filter(family_name__istartswith=racer.family_name[0])
    return {'letters': letters, 'racer':racer }

@register.inclusion_tag('f1info/tags/onthisday.html', takes_context=False)
def show_onthisday():
    current = datetime.datetime.today().strftime("%d.%m")
    for page in Page.objects.all():
        template = page.get_template()
        if template == 'pages/onthisday.html':
            day_field = Content.objects.get_content(page, None, "day")
            if day_field == current:
               return {'page': page, }

@register.inclusion_tag('f1info/tags/fastest_lap.html', takes_context=False)
def show_fastest_lap(gpid):
    heat = Heat.objects.filter(grandprix=gpid, type=Heat.BEST)
    fastest = Result.objects.filter(heat=heat, delta=0)
    return {'objects': fastest, }
