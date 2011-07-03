# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, handler500, handler404, url
from django.conf import settings
from django.contrib import admin
from django.contrib.sitemaps import GenericSitemap
from django.views.generic import list_detail
from pages.models import Page
from easy_news.models import News
from f1info.models import Racer, Engine, Tyre, Team, Track, Season, GrandPrix, Heat, get_alpha
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

racer_list = {
    'queryset' : get_alpha(Racer.objects.all()),
}

racer_info = {
    'queryset' : Racer.objects.all(),
}

racer_ajax_list = {
    'queryset' : Racer.objects.all(),
    'template_name': 'f1info/racer_ajax_list.html',
}

racer_last_info = {
    'queryset' : Racer.objects.all(),
    'template_name': 'f1info/racer_last_info.html',
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

track_info = {
    'queryset': Track.objects.all(),
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
    (r'^drivers/$', list_detail.object_list, racer_list),
    (r'^engines/$', list_detail.object_list, engine_info),
    (r'^tyres/$', list_detail.object_list, tyre_info),
    (r'^teams/$', list_detail.object_list, team_info),
    (r'^tracks/$', list_detail.object_list, track_info),
    (r'^seasons/$', list_detail.object_list, season_info),
    (r'^grandprix/$', list_detail.object_list, grand_prix_info),
    (r'^results/$', list_detail.object_list, heat_info),

    url(r'^drivers/(?P<slug>[-\w]+)/$', list_detail.object_detail, racer_info, name='racer_detail'),
    url(r'^engines/(?P<slug>[-\w]+)/$', list_detail.object_detail, engine_info, name='engine_detail'),
    url(r'^tyres/(?P<slug>[-\w]+)/$', list_detail.object_detail, tyre_info, name='tyre_detail'),
    url(r'^teams/(?P<slug>[-\w]+)/$', list_detail.object_detail, team_info, name='team_detail'),
    url(r'^tracks/(?P<slug>[-\w]+)/$', list_detail.object_detail, track_info, name='track_detail'),
    url(r'^seasons/(?P<slug>[-\w]+)/$', list_detail.object_detail, season_info, name='season_detail'),
    url(r'^grandprix/(?P<object_id>\d{1,9})/$', list_detail.object_detail, grand_prix_info, name='grand_prix_detail'),
    url(r'^results/(?P<slug>[-\w]+)/$', list_detail.object_detail, heat_info, name='heat_detail'),

    url(r'^racer_ajax_list/$', list_detail.object_list, racer_ajax_list, name='racer_ajax_list'),
    url(r'^racer_last_info/(?P<object_id>\d{1,9})/$', list_detail.object_detail, racer_last_info, name='racer_last_info'),

    (r'^admin/', include(admin.site.urls)),
    (r'^robots.txt$', 'django.views.generic.simple.direct_to_template', {'template': 'robots.txt', 'mimetype': 'text/plain'}),
    (r'^googlehostedservice.html$', 'django.views.generic.simple.direct_to_template', {'template': 'google.txt', 'mimetype': 'text/plain'}),
    (r'^sitemap.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    (r'^news/', include('easy_news.urls')),
    (r'^', include('pages.urls')),
    url(r'^markitup/', include('markitup.urls'))
)
