from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin
import os

from tagging.models import TaggedItem
from viewpoint.models import Entry
from staff.models import StaffMember

admin.autodiscover()

handler500 = 'django_ext.views.custom_server_error'

sitemaps = {
}

homepage_entries = {
    'entries': Entry.objects.published,
}

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^blog/', include('viewpoint.urls')),
    url(
        r'^topics/$', 
        'django.views.generic.simple.direct_to_template', 
        {'template':'tagging/index.html'},
        name='tagging_index'
    ),
    url(
        r'^topics/(?P<tag>.+)/$', 
        'django.views.generic.simple.direct_to_template', 
        {'template':'tagging/tag.html'},
        name='tagging_tag'
    ),
    url(
        r'^projects/$', 
        'django.views.generic.simple.direct_to_template', 
        {'template':'github_projects.html'},
        name="projects"
    ),
    url(
        r'^$', 
        'django.views.generic.simple.direct_to_template', 
        {'template':'homepage.html', 'extra_context': homepage_entries},
        name="home"
    ),
    ('', include('djangopypi.urls')),
)


from calloway.urls import urlpatterns as calloway_patterns

urlpatterns += calloway_patterns

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'transmogrify.views.transmogrify_serve',
            {'document_root': os.path.join(os.path.dirname(__file__), 'media')}),
    )
