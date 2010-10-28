# Django settings for project project.

import calloway
import os
import sys

CALLOWAY_ROOT = os.path.abspath(os.path.dirname(calloway.__file__))
sys.path.insert(0, os.path.join(CALLOWAY_ROOT, 'apps'))
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'apps'))
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'lib'))

try:
    from local_settings import DEBUG as LOCAL_DEBUG
    DEBUG = LOCAL_DEBUG
except ImportError:
    DEBUG = False
TEMPLATE_DEBUG = DEBUG

from calloway.settings import *

ADMINS = (
    ('webmaster', 'webmaster@washingtontimes.com'),
)
MANAGERS = ADMINS
DEFAULT_FROM_EMAIL='webdev@washingtontimes.com'
SERVER_EMAIL='webdev@washingtontimes.com'

DATABASES = {
    'default': {
        'NAME': 'dev.db',
        'ENGINE': 'sqlite3',
    },
}

CSRF_COOKIE_DOMAIN = ".washingtontimes.com"
TIME_ZONE = 'America/New_York'
LANGUAGE_CODE = 'en-us'
USE_I18N = True

try:
    from local_settings import MEDIA_URL_PREFIX
except ImportError:
    MEDIA_URL_PREFIX = "/media/"
try:
    from local_settings import MEDIA_ROOT_PREFIX
except ImportError:
    MEDIA_ROOT_PREFIX = os.path.join(PROJECT_ROOT, 'media')
try:    
    from local_settings import MEDIA_ROOT
except ImportError:
    MEDIA_ROOT = os.path.join(MEDIA_ROOT_PREFIX, 'uploads')
try:
    from local_settings import STATIC_ROOT
except ImportError:
    STATIC_ROOT = os.path.join(MEDIA_ROOT_PREFIX, 'static')

MIDDLEWARE_CLASSES = [
    'django.middleware.cache.UpdateCacheMiddleware', 
    'django.middleware.common.CommonMiddleware', 
    'django.contrib.sessions.middleware.SessionMiddleware', 
    'django.middleware.csrf.CsrfViewMiddleware', 
    'django_ext.middleware.cookie.UsernameInCookieMiddleware', 
    'django.contrib.auth.middleware.AuthenticationMiddleware', 
    'django.contrib.messages.middleware.MessageMiddleware', 
    #'django.middleware.gzip.GZipMiddleware', 
    'django.middleware.http.ConditionalGetMiddleware', 
    'django.middleware.csrf.CsrfResponseMiddleware', 
    'django.middleware.doc.XViewMiddleware', 
    #'debug_toolbar.middleware.DebugToolbarMiddleware', 
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware', 
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware', 
    'django.middleware.transaction.TransactionMiddleware', 
    'pagination.middleware.PaginationMiddleware', 
    'ban.middleware.DenyMiddleware', 
    'django.middleware.cache.FetchFromCacheMiddleware',
]

MEDIA_URL = '%suploads/' % MEDIA_URL_PREFIX
STATIC_URL = "%sstatic/" % MEDIA_URL_PREFIX
STATIC_MEDIA_APP_MEDIA_PATH = STATIC_ROOT
STATIC_MEDIA_COPY_PATHS = (
    {'from': os.path.join(CALLOWAY_ROOT, 'media'), 'to': STATIC_ROOT},
    {'from': 'static', 'to': STATIC_ROOT},
)
STATIC_MEDIA_COMPRESS_CSS = not DEBUG
STATIC_MEDIA_COMPRESS_JS = not DEBUG

MMEDIA_DEFAULT_STORAGE = 'media_storage.MediaStorage'
MMEDIA_IMAGE_UPLOAD_TO = 'image/%Y/%m/%d'

AUTH_PROFILE_MODULE = ''

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_ROOT, 'templates'),
) + CALLOWAY_TEMPLATE_DIRS

CACHE_BACKEND = 'memcached://localhost:11211/'

INSTALLED_APPS = APPS_CORE + \
    APPS_ADMIN + \
    APPS_STAFF + \
    APPS_REVERSION + \
    APPS_CALLOWAY_DEFAULT + \
    APPS_MPTT + \
    APPS_CATEGORIES + \
    APPS_COMMENT_UTILS + \
    APPS_FRONTEND_ADMIN + \
    APPS_MEDIA + \
    APPS_UTILS + \
    APPS_REGISTRATION + \
    APPS_TINYMCE + (
        "viewpoint",
        "profiles",
        "typogrify",
        "transmogrify",
        'disqus',
    )

TEMPLATE_CONTEXT_PROCESSORS = [
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'context_processors.global_settings',
    'staticmediamgr.context_processor.static_url',
]

ADMIN_TOOLS_THEMING_CSS = 'admin/css/theming.css'
ADMIN_TOOLS_MENU = 'menu.CustomMenu'

TINYMCE_JS_URL = '%sjs/tiny_mce/tiny_mce.js' % STATIC_URL
TINYMCE_JS_ROOT = os.path.join(STATIC_ROOT, 'js/tiny_mce')

MMEDIA_DEFAULT_STORAGE = 'media_storage.MediaStorage'
MMEDIA_IMAGE_UPLOAD_TO = 'image/%Y/%m/%d'

VIEWPOINT_DEFAULT_STORAGE = 'media_storage.MediaStorage'
TOPICS_DEFAULT_STORAGE = 'media_storage.MediaStorage'

VIEWPOINT_DEFAULT_BLOG = 'default'
VIEWPOINT_AUTHOR_MODEL = 'staff.staffmember'

DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    # 'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    # 'debug_toolbar.panels.headers.HeaderDebugPanel',
    # 'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    # 'debug_toolbar.panels.template.TemplateDebugPanel',
    # 'debug_toolbar.panels.sql.SQLDebugPanel',
    # 'debug_toolbar.panels.logger.LoggingPanel',
)
DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False
}

NATIVE_TAGS = (
    'apps.tags',
)

TINYMCE_DEFAULT_CONFIG = {
    'theme': "advanced",
    'relative_urls': False,
    'plugins': "safari,paste,advimage,advlink,preview,fullscreen,searchreplace,icode",
    'theme_advanced_toolbar_location' : "top",
    'theme_advanced_toolbar_align' : "left",
    'theme_advanced_buttons1' : "formatselect,bold,italic,underline,strikethrough,blockquote,|,bullist,numlist,|,link,unlink,|,charmap,image,media,pastetext,pasteword,search,replace,icode,|,code,fullscreen,preview",
    'theme_advanced_buttons2' : "",
    'theme_advanced_buttons3' : "",
    'theme_advanced_statusbar_location' : "bottom",
    'width': "600",
    'height': "600",
}

# TINYMCE_ADMIN_FIELDS = {
#     'stories.story': ('body',),
#     'staff.staffmember': ('bio',),
#     'flatpages.flatpage': ('content',),
# }



try:
    from local_settings import *
except ImportError:
    pass
