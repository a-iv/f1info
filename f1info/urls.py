# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, handler500, handler404, url
from django.conf import settings
from django.contrib import admin
from django.contrib.sitemaps import GenericSitemap
from django.views.generic import list_detail
from pages.models import Page
from easy_news.models import News
from f1info.models import Racer, Engine, Tyre, Team, Season, GrandPrix, Heat
admin.autodiscover()

handler500 # Pyflakes

urlpatterns = patterns('')

pages_dict = {
    'queryset': Page.objects.exclude(status=Page.DRAFT),
    'date_field': 'last_modification_date',
}

news_dict = {
    'queryset': News.objects.filter(show=True),
    'date_field': 'date',
}

sitemaps = {
    'pages': GenericSitemap(pages_dict),
    'news': GenericSitemap(news_dict),
}

racer_info = {
    'queryset' : Racer.objects.all(),
}

engine_info = {
    'queryset': Engine.objects.all(),
}

tyre_info = {
    'queryset': Tyre.objects.all(),
}

team_info = {
    'queryset': Team.objects.all(),
}

season_info = {
    'queryset': Season.objects.all(),
}

grand_prix_info = {
    'queryset': GrandPrix.objects.all(),
}

heat_info = {
    'queryset': Heat.objects.all(),
}

if settings.DEBUG:
    pass

urlpatterns += patterns('', (r'^', include('config.urls')))
urlpatterns += patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
     {'document_root': settings.MEDIA_ROOT}),
)


urlpatterns += patterns(
    '',
    (r'^racer/$', list_detail.object_list, racer_info),
    (r'^engine/$', list_detail.object_list, engine_info),
    (r'^tyre/$', list_detail.object_list, tyre_info),
    (r'^team/$', list_detail.object_list, team_info),
    (r'^season/$', list_detail.object_list, season_info),
    (r'^grand_prix/$', list_detail.object_list, grand_prix_info),
    (r'^heat/$', list_detail.object_list, heat_info),

    url(r'^racer/(?P<object_id>\d{1,9})/$', list_detail.object_detail, racer_info, name='racer_detail'),
    url(r'^engine/(?P<object_id>\d{1,9})/$', list_detail.object_detail, engine_info, name='engine_detail'),
    url(r'^tyre/(?P<object_id>\d{1,9})/$', list_detail.object_detail, tyre_info, name='tyre_detail'),
    url(r'^team/(?P<object_id>\d{1,9})/$', list_detail.object_detail, team_info, name='team_detail'),
    url(r'^season/(?P<object_id>\d{1,9})/$', list_detail.object_detail, season_info, name='season_detail'),
    url(r'^grand_prix/(?P<object_id>\d{1,9})/$', list_detail.object_detail, grand_prix_info, name='grand_prix_detail'),
    url(r'^heat/(?P<object_id>\d{1,9})/$', list_detail.object_detail, heat_info, name='heat_detail'),

    (r'^', include('pages_link.urls')), # Before admin.site.root
    (r'^admin/filebrowser/', include('filebrowser.urls')),
    (r'^admin/(.*)', admin.site.root),
    (r'^tinymce/', include('tinymce.urls')),
    (r'^robots.txt$', 'django.views.generic.simple.direct_to_template', {'template': 'robots.txt', 'mimetype': 'text/plain'}),
    (r'^sitemap.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    (r'^news/', include('easy_news.urls')),
    (r'^photologue/', include('photologue.urls')),
    (r'^', include('pages.urls')),
#    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
)
