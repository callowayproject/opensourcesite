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
    'staffmembers': StaffMember.objects.filter(is_active=True)
}

tagged_models = (dict(
    title="Blog Posts",
    query=lambda tag: TaggedItem.objects.get_by_model(Entry, tag).filter(public=True),
  ),
)

tagging_ext_kwargs = {
  'tagged_models':tagged_models,
}

post_tag_kwargs = {'model':'entry'}
post_tag_kwargs.update(tagging_ext_kwargs)

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^blog/', include('viewpoint.urls')),
    url(
        r'^post/tags/(?P<tag>.+)', 
        'tagging_ext.views.tag_by_model',
        kwargs=post_tag_kwargs, 
        name='tagging_ext_tag_by_model'
    ),
    url(
        r'^tags/$', 
        'tagging_ext.views.index', 
        name='tagging_ext_index'
    ),
    url(
        r'^tags/(?P<tag>.+)/$', 
        'tagging_ext.views.tag',
        kwargs=tagging_ext_kwargs, 
        name='tagging_ext_tag'
    ),
    url(
        r'^tags/(?P<tag>.+)/(?P<model>.+)$', 
        'tagging_ext.views.tag_by_model',
        kwargs=tagging_ext_kwargs, 
        name='tagging_ext_tag_by_model'
    ),
    url(
        r'^$', 
        'django.views.generic.simple.direct_to_template', 
        {'template':'homepage.html', 'extra_context': homepage_entries},
        name="home"
    ),
)
from calloway.urls import urlpatterns as calloway_patterns

urlpatterns += calloway_patterns

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'transmogrify.views.transmogrify_serve',
            {'document_root': os.path.join(os.path.dirname(__file__), 'media')}),
    )
