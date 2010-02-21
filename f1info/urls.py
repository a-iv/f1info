
from django.conf.urls.defaults import patterns, include, handler500, handler404
from django.conf import settings
from django.contrib import admin
from django.contrib.sitemaps import GenericSitemap
from pages.models import Page
admin.autodiscover()

handler500 # Pyflakes

urlpatterns = patterns('')

pages_dict = {
    'queryset': Page.objects.exclude(status=Page.DRAFT),
    'date_field': 'last_modification_date',
}

sitemaps = {
    'pages': GenericSitemap(pages_dict),
}

if settings.DEBUG:
    urlpatterns += patterns('', (r'^', include('config.urls')))
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )

urlpatterns += patterns(
    '',
    (r'^admin/(.*)', admin.site.root),
    (r'^tinymce/', include('tinymce.urls')),
    (r'^robots.txt$', 'django.views.generic.simple.direct_to_template', {'template': 'robots.txt', 'mimetype': 'text/plain'}),
    (r'^sitemap.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    (r'^', include('pages.urls')),
#    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
)
