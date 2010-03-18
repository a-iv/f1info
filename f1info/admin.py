# -*- coding: utf-8 -*-

from django.contrib import admin
from f1info.models import Racer, Engine, Team, Tyre, Season, Point, Country
from f1info.models import GrandPrix, Heat, Result, BestLap

class ModelAdmin(admin.ModelAdmin):
    class Media:
        js = (
            '/media/js/jquery-1.3.2.min.js',
            '/media/js/jquery.bgiframe.min.js',
            '/media/js/jquery.sexy-combo-2.1.2.min.js',
            '/media/js/admin.js',
        )
        css = {
            'all': (
                '/media/css/sexy.css',
                '/media/css/sexy-combo.css',
                '/media/css/admin.css',
            ),
        }

class CountryAdmin(ModelAdmin):
    pass

try:
    admin.site.register(Country, CountryAdmin)
except admin.sites.AlreadyRegistered:
    pass

class RacerAdmin(ModelAdmin):
    prepopulated_fields = {'slug': ('first_name', 'family_name',)}

try:
    admin.site.register(Racer, RacerAdmin)
except admin.sites.AlreadyRegistered:
    pass

class EngineAdmin(ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

try:
    admin.site.register(Engine, EngineAdmin)
except admin.sites.AlreadyRegistered:
    pass

class TeamAdmin(ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

try:
    admin.site.register(Team, TeamAdmin)
except admin.sites.AlreadyRegistered:
    pass

class TyreAdmin(ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

try:
    admin.site.register(Tyre, TyreAdmin)
except admin.sites.AlreadyRegistered:
    pass

class PointInline(admin.TabularInline):
    model = Point
    extra = 10

class GrandPrixInline(admin.TabularInline):
    prepopulated_fields = {'slug': ('season', 'name',)}
    model = GrandPrix
    extra = 10

class SeasonAdmin(ModelAdmin):
    inlines = [
        PointInline,
        GrandPrixInline,
    ]

try:
    admin.site.register(Season, SeasonAdmin)
except admin.sites.AlreadyRegistered:
    pass

class ResultInline(admin.TabularInline):
    model = Result
    extra = 24
    exclude = ['_points_count']

class BestLapInline(admin.TabularInline):
    model = BestLap
    extra = 1
    max_num = 1

class HeatAdmin(ModelAdmin):
    prepopulated_fields = {'slug': ('grandprix', 'type',)}
    inlines = [
        ResultInline,
        BestLapInline,
    ]

try:
    admin.site.register(Heat, HeatAdmin)
except admin.sites.AlreadyRegistered:
    pass
