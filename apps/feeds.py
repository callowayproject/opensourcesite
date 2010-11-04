from datetime import datetime

from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.contrib.auth.models import User
from django.template.defaultfilters import linebreaks, escape, capfirst

from viewpoint.models import Entry
from viewpoint.feeds import LatestEntries
from tagging.models import Tag, TaggedItem

ITEMS_PER_FEED = 20


class TagFeed(LatestEntries):
    def get_object(self, params):
        return get_object_or_404(Tag, name=params[0].lower())
    
    def feed_id(self, tag):
        return 'http://%s/feeds/posts/with_tag/%s/' % (
            Site.objects.get_current().domain,
            tag.name,
        )

    def feed_title(self, tag):
        return 'Blog post feed for tag %s' % tag.name

    def feed_updated(self, tag):
        t = Tag.objects.get(name__iexact=tag.name)
        return TaggedItem.objects.get_union_by_model(Entry, t).latest('pub_Date').pub_date

    def feed_links(self, tag):
        absolute_url = reverse('tag_list', kwargs={'app': 'viewpoint', 'tag': tag})
        complete_url = "http://%s%s" % (
                Site.objects.get_current().domain,
                absolute_url,
            )
        return ({'href': complete_url},)

    def items(self, tag):
        t = Tag.objects.get(name__iexact=tag.name)
        return TaggedItem.objects.get_union_by_model(Entry.objects.order_by('-pub_date'), t)