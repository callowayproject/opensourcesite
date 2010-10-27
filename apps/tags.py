import os
try:
    from hashlib import sha1 as sha
except ImportError:
    from sha import sha
import Image
from staff.models import StaffMember
from django.conf import settings

def staff_members():
    return StaffMember.objects.filter(is_active=True)
staff_members.function = True

def github_projects():
    import json, urllib2
    url = "http://github.com/api/v2/json/repos/show/washingtontimes"
    try:
        result = urllib2.urlopen(url)
    except urllib2.HTTPError, e:
        print e
        return []
    pyresult = json.loads(result.read())
    return pyresult['repositories'][:]
github_projects.function = True

def blog_entry_years(blog):
    return blog.entry_set.dates('pub_date', 'year')
blog_entry_years.function = True

def blog_entry_months(blog, year):
    return blog.entry_set.filter(pub_date__year=year).dates('pub_date', 'month')
blog_entry_months.function = True

def blog_entry_yearmonths(blog):
    return blog.entry_set.dates('pub_date', 'month')
blog_entry_yearmonths.function = True

def blog_authors(blog):
    authors = blog.entry_set.distinct().values_list('author', flat=True).order_by('author')
    return StaffMember.objects.filter(pk__in=authors)
blog_authors.function = True

def smart_fit(image_field, width=20000, height=20000):
    """
    Given a width, height or both, it will return the width and height to 
    fit in the given area.
    """
    try:
        if not os.path.exists(image_field.path):
            return 0, 0
    except ValueError:
        return 0, 0
    im = Image.open(image_field.path)
    im_width, im_height = im.size

    if width==20000 and height==20000:
        return im_width, im_height
    elif width is None:
        width = 20000
    elif height is None:
        height = 20000
    
    im_scale = float(im_width)/float(im_height)
    scale = float(width)/float(height)
    
    if im_scale > scale:
        ratio = float(width)/float(im_width)
        width = int(round(ratio * im_width))
        height = int(round(ratio * im_height))
    else:
        ratio = float(height)/float(im_height)
        width = int(round(ratio * im_width))
        height = int(round(ratio * im_height))
    
    return width, height

def smart_size(image_field, size_string, **kwargs):
    """
    Given an image field and size string, return an img tag
    """
    bits = size_string.split("x")
    attributes = ['%s="%s"' % (key, val) for key, val in kwargs.items()]
    
    if len(bits) == 1 or not bits[1]:
        fit_to_width = int(bits[0])
        fit_to_height = 20000
    elif not bits[0]:
        fit_to_height = int(bits[1])
        fit_to_width = 20000
    else:
        fit_to_width, fit_to_height = map(int, bits)
    try:
        if not hasattr(image_field, 'path') or not os.path.exists(image_field.path):
            return '<img height="%s" width="%s" src="%simg_not_found" %s />'\
                % (bits[1], bits[0], settings.STATIC_URL, " ".join(attributes))
    except ValueError:
        return '<img src="img_not_found" />'
    fit_to_width, fit_to_height = smart_fit(image_field, fit_to_width, fit_to_height)
    prefix, ext = os.path.splitext(image_field.url)
    
    size = "_s%sx%s" % (fit_to_width, fit_to_height)
    
    security_hash = sha(size+settings.MOGRIFY_KEY).hexdigest()
    
    url = "%s%s%s?%s" % (prefix, size, ext, security_hash)
    
    img_tag = '<img src="%s" width="%s" height="%s" %s />' % (
        url, fit_to_width, fit_to_height, " ".join(attributes)
    )
    return img_tag
smart_size.function = 1
