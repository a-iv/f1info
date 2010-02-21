from django.contrib import admin
from django.contrib.admin.sites import NotRegistered, AlreadyRegistered
from pages.models import Page
from pages.admin import PageAdmin

class NewPageAdmin(PageAdmin):
    class Media:
        js = ('js/pages_slug.js', )

try:
    admin.site.unregister(Page)
except NotRegistered:
    pass

try:
    admin.site.register(Page, NewPageAdmin)
except AlreadyRegistered:
    pass
