# -*- coding: utf-8 -*-

import os

gettext_noop = lambda s: s

ADMINS = (
    ('f1online', 'mansellfan@gmail.com'),
    ('alexander','alexander.vl.ivanov@gmail.com'),
)

MANAGERS = ADMINS

EMAIL_SUBJECT_PREFIX = '[f1online]'

DATABASE_ENGINE = 'postgresql_psycopg2'    # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'f1info'
DATABASE_USER = 'f1info'             # Not used with sqlite3.
DATABASE_PASSWORD = 'password'         # Not used with sqlite3.
DATABASE_HOST = 'localhost'             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = '5432'             # Set to empty string for default. Not used with sqlite3.

TIME_ZONE = 'Asia/Yekaterinburg'

LANGUAGE_CODE = 'ru'

SITE_ID = 1

MEDIA_ROOT = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'media')
UPLOAD_DIR = 'upload'

MEDIA_URL = '/media/'
UPLOAD_URL = os.path.join(MEDIA_URL, UPLOAD_DIR)


ADMIN_MEDIA_PREFIX = '/media/admin/'

SECRET_KEY = '_7y*-5^h4*^4b0=n%kwtw*1a(fd%!lq8xbx-#nc*8v5ba4-*te'

MIDDLEWARE_CLASSES = [
    'django.middleware.common.CommonMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
    'modelurl.middleware.ModelUrlMiddleware',

]

ROOT_URLCONF = 'f1info.urls'


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.redirects',
    'django.contrib.sitemaps',
    'django.contrib.markup',
    'config',
    'pages',
    'chunks',
    'tagging',
    'imagekit',
    'easy_news',
    'modelurl',
    'urlmethods',
    'menuproxy',
    'utilities',
    'attachment',
    'f1info.custom_attachment',
    'seo',
    'south',
    'markitup',
    'f1info',
    'f1info.info',
    'authority',
)

TEMPLATE_LOADERS = [
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
    'django.template.loaders.eggs.load_template_source',
]

TEMPLATE_DIRS = [
    os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates'),
]

FIXTURE_DIRS = [
    os.path.join(os.path.dirname(os.path.dirname(__file__)), 'fixtures'),
]

TEMPLATE_CONTEXT_PROCESSORS = [
    'django.core.context_processors.auth',
    'django.core.context_processors.i18n',
    'django.core.context_processors.debug',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'pages.context_processors.media',
]


# Server settings
FORCE_SCRIPT_NAME = ''

CACHE_BACKEND = 'locmem:///?max_entries=5000'

# django-hex-storage
DEFAULT_FILE_STORAGE = 'hex_storage.HexFileSystemStorage'


# django-modelurl
MODELURL_MODELS = [
    {'model': 'easy_news.models.News', },
    {'model': 'pages.models.Page', },
]

MODELURL_VIEWS = [
    {
        'view': 'django.contrib.admin.site.root',
        'disable': True,
    },
    {
        'view': 'pages.views.details',
        'context': 'current_page',
    },
]

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
    ('pages/soon.html', u'Скоро'),
    ('pages/frontpage.html', u'Главная страница'),
    ('pages/articles.html', u'Статьи'),
    ('pages/onthisday.html', u'В этот день'),
)

# django-config settings
CONFIG_SITES = ['www.f1online.ru', ]
CONFIG_REDIRECTS = ['f1online.ru', ]
CONFIG_APP_MEDIA = {
    'pages': [
        ('pages', 'pages',),
    ]
}

# django-menu-proxy
MENU_PROXY_RULES = [
    {
        'name': 'news_list',
        'method': 'insert',
        'proxy': 'menuproxy.proxies.ReverseProxy',
        'viewname': 'news_list',
        'title_text': u'Новости',
    },
    {
        'name': 'pages',
        'method': 'children',
        'proxy': 'menuproxy.proxies.MenuProxy',
        'model': 'pages.models.Page',
        'children_filter': {'status': 1, },
        'ancestors_exclude': {'status': 0, },
    },
    {
        'name': 'results',
        'method': 'insert',
        'proxy': 'menuproxy.proxies.StaticUrlProxy',
        'url_text': '/season/',
        'title_text': u'Результаты',
    },
]
EASY_NEWS_MENU_LEVEL = 0


# SEO settings
SEO_FOR_MODELS = [
    'pages.models.Page',
    'easy_news.models.News',
]

# Easy news settings
EASY_NEWS_MENU_LEVEL = 1
NEWS_TAGGING = False

# django-tinymce-attachment
ATTACHMENT_FOR_MODELS = [
    'pages.models.Page',
    'easy_news.models.News',
]

ATTACHMENT_LINK_MODELS = [
    'pages.models.Page',
    'easy_news.models.News',
]

ATTACHMENT_IKSPECS = 'f1info.custom_attachment.ikspecs'

MARKITUP_SET = 'markitup/sets/markdown'
MARKITUP_FILTER = ('markdown.markdown', {'safe_mode': True})
MARKITUP_AUTO_PREVIEW = False
