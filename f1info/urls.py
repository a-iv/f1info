
from django.conf.urls.defaults import patterns, include, handler500, handler404
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

handler500 # Pyflakes

urlpatterns = patterns('')

if settings.DEBUG:
    urlpatterns += patterns('', (r'^', include('config.urls')))
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )

urlpatterns += patterns(
    '',
    (r'^admin/(.*)', admin.site.root),
#    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
)
