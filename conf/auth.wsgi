import os, sys, site

site.addsitedir('/home/webdev/.virtualenvs/osv2/lib/python2.6/site-packages')

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(PROJECT_ROOT,"apps"))
sys.path.insert(0, os.path.join(PROJECT_ROOT,"lib"))
sys.path.insert(0, PROJECT_ROOT)

sys.stdout = sys.stderr
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django.contrib.auth.models import User
from django import db

def check_password(environ, user, password):
    db.reset_queries() 

    kwargs = {'username': user, 'is_active': True} 

    try: 
        try: 
            user = User.objects.get(**kwargs) 
        except User.DoesNotExist: 
            return None

        if user.check_password(password): 
            return True
        else: 
            return False
    finally: 
        db.connection.close() 
