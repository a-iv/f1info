# -*- coding: utf-8 -*-

import os

gettext_noop = lambda s: s

ADMINS = (
    ('webmaster', 'webmaster@redsolution.ru'),
)

MANAGERS = ADMINS

EMAIL_SUBJECT_PREFIX = '[f1info]'

DATABASE_ENGINE = 'postgresql_psycopg2'    # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'f1info'
DATABASE_USER = 'f1info'             # Not used with sqlite3.
DATABASE_PASSWORD = 'password'         # Not used with sqlite3.
DATABASE_HOST = 'localhost'             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = '5432'             # Set to empty string for default. Not used with sqlite3.

TIME_ZONE = 'Asia/Yekaterinburg'

LANGUAGE_CODE = 'ru'

SITE_ID = 1

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/admin_media/'

# Don't share this with anybody.
SECRET_KEY = '_7y*-5^h4*^4b0=n%kwtw*1a(fd%!lq8xbx-#nc*8v5ba4-*te'

MIDDLEWARE_CLASSES = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
]

ROOT_URLCONF = 'f1info.urls'


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.markup',
    'config',
    'mptt',
    'pages',
    'chunks',
    'imagekit',
    #'pages_link',
    'pages_seo',
    'easy_news',
    'hex_storage',
    'photologue',
    'filebrowser',
    'south',
    'f1info',
    'f1info.custom_admin',
    'f1info.custom_pages',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates'),
)

FIXTURE_DIRS = (
    os.path.join(os.path.dirname(os.path.dirname(__file__)), 'fixtures'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.i18n',
    'django.core.context_processors.debug',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'pages.context_processors.media',
)

# Server settings
FORCE_SCRIPT_NAME = ''

CACHE_BACKEND = 'locmem:///?max_entries=5000'

# django-config settings
CONFIG_SITES = ['www.f1info.ru', ]
CONFIG_REDIRECTS = ['f1info.ru', ]
CONFIG_APP_MEDIA = {
    'pages': [
        ('pages', 'pages',),
    ]
}
#CONFIG_NEED_AUTH = True

# Pages CMS settings
PAGE_TAGGING = False
PAGE_PERMISSION = False
PAGE_TINYMCE = False
PAGE_HIDE_ROOT_SLUG = True
PAGE_LANGUAGES = (
    ('ru', gettext_noop('Russian')),
    ('en', gettext_noop('English')),
)
DEFAULT_PAGE_TEMPLATE = 'pages/index.html'
PAGE_TEMPLATES = (
#    ('pages/frontpage.html', gettext_noop('frontpage')),
)
PAGE_CONNECTED_MODELS = [
    {
        'model': 'pages_seo.models.PagesSeo',
        'form': 'pages_seo.forms.PagesSeoForm',
        'options': {
            'max_num': 1,
        },
    },
]

#django-hex-storage
DEFAULT_FILE_STORAGE = 'hex_storage.HexFileSystemStorage'

# Photologue
PHOTOLOGUE_DIR = os.path.join('upload', 'photologue')

#django-filebroser
FILEBROWSER_URL_WWW = '/media/upload/filebrowser/'
FILEBROWSER_PATH_SERVER = os.path.join(MEDIA_ROOT, 'upload', 'filebrowser')
FILEBROWSER_URL_FILEBROWSER_MEDIA = '/media/filebrowser/'

try:
    from localsettings import *
except ImportError:
    pass
