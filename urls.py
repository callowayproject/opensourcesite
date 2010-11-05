from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin
import os

from tagging.models import TaggedItem
from feeds import TagFeed
from viewpoint.models import Entry
from viewpoint.feeds import LatestEntries
from staff.models import StaffMember

admin.autodiscover()

handler500 = 'django_ext.views.custom_server_error'

sitemaps = {
}

homepage_entries = {
    'entries': Entry.objects.published,
}

urlpatterns = patterns('django.views.generic.simple',
	('blog/post/coordt/2010/07/django-alphabet-filter-released-international-char/','redirect_to', {'url': '/blog/2010/jul/28/django-alphabet-filter-released-international-char/'}),
	('blog/post/coordt/2010/07/creating-alphabetical-filter-djangos-admin/','redirect_to', {'url': '/blog/2010/jul/15/creating-alphabetical-filter-djangos-admin/'}),
	('blog/post/coordt/2010/02/loading-templates-based-request-headers-django/', 'redirect_to', {'url': '/blog/2010/feb/17/loading-templates-based-request-headers-django/'}),
	('blog/post/coordt/2010/01/how-we-create-and-deploy-sites-fast-virtualenv-and/', 'redirect_to', {'url': '/blog/2010/jan/8/how-we-create-and-deploy-sites-fast-virtualenv-and/'}),
	('blog/post/coordt/2010/01/what-difference-year-makes/', 'redirect_to', {'url': '/blog/2010/jan/6/what-difference-year-makes/'}),
	('blog/post/coordt/2009/12/django-object-permissions-proof-concept/', 'redirect_to', {'url': '/blog/2009/dec/10/django-object-permissions-proof-concept/'}),
	('blog/post/jquick/2009/09/django-sql-debug-comments/', 'redirect_to', {'url': '/blog/2009/sep/15/django-sql-debug-comments/'}),
	('blog/post/coordt/2009/09/request-comments-auto-installation-apps-django/', 'redirect_to', {'url': '/blog/2009/sep/15/request-comments-auto-installation-apps-django/'}),
	('blog/post/jquick/2009/05/django-district-meetup/', 'redirect_to', {'url': '/blog/2009/may/3/django-district-meetup/'}),
	('blog/post/coordt/2009/04/interesting-ie6-trend/', 'redirect_to', {'url': '/blog/2009/apr/21/interesting-ie6-trend/'}),
	('blog/post/jquick/2009/03/apibuilder-open-your-content-all-see/', 'redirect_to', {'url': '/blog/2009/mar/24/apibuilder-open-your-content-all-see/'}),
	('blog/post/jsoares/2009/03/djangotidbits/', 'redirect_to', {'url': '/blog/2009/mar/21/djangotidbits/'}),
	('blog/post/coordt/2009/02/training-video-week/', 'redirect_to', {'url': '/blog/2009/feb/26/training-video-week/'}),
	('blog/post/coordt/2009/02/washington-times-releases-open-source-projects/', 'redirect_to', {'url': '/blog/2009/feb/19/washington-times-releases-open-source-projects/'}),
	('blog/post/coordt/2009/02/training-video-week/', 'redirect_to', {'url': '/blog/2009/feb/12/training-video-week/'}),
	('blog/post/jsoares/2009/02/will-work-fun/', 'redirect_to', {'url': '/blog/2009/feb/12/will-work-fun/'}),
	('blog/post/jquick/2009/02/making-django-unit-tests-work-you/', 'redirect_to', {'url': '/blog/2009/feb/11/making-django-unit-tests-work-you/'}),
	('blog/post/coordt/2009/02/create-stand-alone-django-documentation-browser/', 'redirect_to', {'url': '/blog/2009/feb/9/create-stand-alone-django-documentation-browser/'}),
	('blog/post/coordt/2009/01/training-video-week/', 'redirect_to', {'url': '/blog/2009/jan/29/training-video-week/'}),
	('blog/post/jsoares/2009/01/im-lazier-then-django-forms/', 'redirect_to', {'url': '/blog/2009/jan/17/im-lazier-then-django-forms/'}),
	('blog/post/coordt/2009/01/training-video-week/', 'redirect_to', {'url': '/blog/2009/jan/15/training-video-week/'}),
	('blog/post/coordt/2009/01/generic-collections-django/', 'redirect_to', {'url': '/blog/2009/jan/12/generic-collections-django/'}),
	('blog/post/coordt/2008/12/how-i-set-my-development-mac/', 'redirect_to', {'url': '/blog/2008/dec/26/how-i-set-my-development-mac/'}),
)

urlpatterns += patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^blog/', include('viewpoint.urls')),
    url(
        r'^feeds/posts/all/$',
        'django.contrib.syndication.views.feed',
        {'feed_dict': {'all': LatestEntries}, 'url': 'all'},
        name="rss_feed"
    ),
    url(
        r'^feeds/posts/(?P<url>.+)/$',
        'django.contrib.syndication.views.feed',
        {'feed_dict': {'with_tag': TagFeed},},
        name="rss_tag_feed"
    ),
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
