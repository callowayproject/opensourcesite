from staff.models import StaffMember

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