from __future__ import with_statement
from fabric.api import sudo, env, run, settings, hide, require, abort, cd, local
from fabric.contrib.files import append, exists
from fabric.contrib.project import rsync_project
from fabric.decorators import hosts
import os
from local_fab_vars import (project_path, project_owner, 
                            venv_path, venv, site_path, site_name)

apache_pkgs = {
    'ubuntu': ('apache2','apache2.2-common','apache2-mpm-worker',
               'apache2-utils','libapache2-mod-wsgi',)
}

python_pkgs = {
    'ubuntu': ('virtualenvwrapper','virtualenv')
}

pg_pkgs = {
    'ubuntu': ('postgresql-client-8.4', 'postgresql-client-common')
}

scm_pkgs = {
    'ubuntu': ('libcurl3-dev','libxslt-dev','curl','subversion','mercurial')
}

sys_pkgs = {
    'ubuntu': ('tidy','python-setuptools','python-dev','python-psycopg2',
    'python-pip','python-imaging','libjpeg-progs','fabric','vim','htop',
    'nfs-common','ntp')
}

required_pkgs = {
    'ubuntu': apache_pkgs['ubuntu'] + sys_pkgs['ubuntu'] + pg_pkgs['ubuntu'] + scm_pkgs['ubuntu']
}

server_cmds = {
    'ubuntu': {
        'install_pkg': 'apt-get install -ym %(package)s',
        'list_pkgs': 'dpkg --get-selections | grep ^%(package)s[[:space:]]'
    }
}

wsgi_path = 'conf/osv2.wsgi'

def set_env(**kwargs):
    for i in kwargs.items():
        setattr(env, *i)
    
    
def has_package(os, package):
    """
    Check if the server has the package installed
    """
    if isinstance(package, basestring):
        pkgs = package.split(' ')
    else:
        pkgs = package
    
    final_output = []
    has_everything = True
    list_pkg_cmd = server_cmds[os]['list_pkgs']
    with settings(
        hide('warnings', 'running', 'stdout', 'stderr'),
        warn_only=True
    ):
        for item in pkgs:
            if '%(package)s' in list_pkg_cmd:
                output = run(list_pkg_cmd % {'package': item})
            elif '%s' in list_pkg_cmd:
                output = run(list_pkg_cmd % item)
            else:
                output = run('%s %s' % (list_pkg_cmd, item))
            final_output.append(output)
            has_everything = not output.failed
    return has_everything


def install_os_packages(os, packages):
    if isinstance(packages, basestring):
        pkgs = packages.split(' ')
    else:
        pkgs = packages
    failed_pkgs = []
    with settings(
        hide('warnings', 'running', 'stdout', 'stderr'),
        warn_only=True
    ):
        for pkg in pkgs:
            if not has_package(os, pkg):
                print "Installing %s" % pkg
                if '%(package)s' in server_cmds[os]['install_pkg']:
                    output = sudo(server_cmds[os]['install_pkg'] % {'package': pkg})
                elif '%s' in server_cmds[os]['install_pkg']:
                    output = sudo(server_cmds[os]['install_pkg'] % pkg)
                else:
                    output = sudo('%s %s' % (server_cmds[os]['install_pkg'], pkg))
                if output.failed:
                    failed_pkgs.append(pkg)
    if failed_pkgs:
        print "The following packages didn't install:"
        for item in failed_pkgs:
            print '\t', item

def install_pip():
    if not has_package('ubuntu', 'python-pip'):
        env.has_pip = False
        return
    with settings(
        hide('warnings', 'running', 'stdout', 'stderr'),
        warn_only = True
    ):
        output = run('which pip')
        if output:
            env.has_pip = True
            return
        output = sudo('easy_install pip')
        env.has_pip = not output.failed

def install_python_pkgs(packages, virtualenv=None, **kwargs):
    set_env(**kwargs)
    require('has_pip', provided_by=[install_pip,])
    if not env.has_pip:
        abort("pip is not installed, so the python packages can't be installed.")
    if isinstance(packages, (list, tuple)):
        pkgs = ' '.join(packages)
    else:
        pkgs = packages
    venv = ' -E %s ' % virtualenv if virtualenv else ' '
    sudo('pip install%s%s' % (venv, pkgs))

    
def install_git_scripts():
    if exists('git-scripts'):
        print "Updating the git scripts."
        with cd('git-scripts'): run('git pull origin master')
    else:
        run('git clone http://opensource.washingtontimes.com/git/public/git-scripts.git/')
    with cd('git-scripts'):
        sudo('./linkscripts')

def link_apache_conf(site_name):
    sudo('ln -s %(site_path)s/conf/apache2-%(site_name)s /etc/apache2/sites-available/%(site_name)s' % {'site_path': site_path, 'site_name':site_name})

def enable_site(site_name):
    sudo('a2ensite %s' % site_name)
    sudo('/etc/init.d/apache2 restart')


def setup(**kwargs):
    os = kwargs.pop('os','ubuntu')
    if kwargs:
        set_env(**kwargs)
    print "Installing OS packages"
    install_os_packages(os, required_pkgs[os])
    compile_git()
    install_pip()
    install_python_pkgs(python_pkgs[os])
    install_git_scripts()
    sudo('mkdir -p %s' % project_path)

def compile_git():
    if not exists('/usr/local/bin/git'):
        run('wget http://kernel.org/pub/software/scm/git/git-1.7.3.2.tar.gz')
        run('tar xvfz git-1.7.1.tar.gz')
        with cd('git-1.7.1'):
            run('./configure --with-curl --without-tcltk | grep curl')
            run('make')
            sudo('make install')
    else:
        print "git is already installed."
    
def deploy(url, host=None):
    """
    Set up the website on a server. Assumes all the setup has been done.
    
    The url is the git repository for the code
    """
    if host:
        print "setting hosts"
        set_env(hosts=[host,])
    
    if not exists(site_path):
        with cd(project_path):
            sudo('git clone %s %s' % (url, site_name))
    if not exists(venv_path):
        run('mkdir %s' % venv_path)
    sudo('chown -R %s %s' % (project_owner, site_path))
    with cd(site_path):
        run('source virtualenvwrapper.sh; mkvirtualenv %s' % site_name)
        run('%s/bin/pip install -E %s -r setup/requirements.txt' % (venv, venv))
    link_apache_conf(site_name)
    enable_site(site_name)

def update():
    """
    Cause the site to pull in the latest changes to its code and touch the
    wsgi file so it reloads
    """
    with cd(site_path):
        run('git pull --all')
    reload()

def install_pkg(package, version=None):
    """
    Install a package. Ideally should be in the format pkgname==vnum
    """
    import re
    if not hasattr(env, 'updated_reqs'):
        set_env(updated_reqs=False)
    
    remote_python = os.path.join(venv, 'bin', 'python')
    remote_pip = os.path.join(venv, 'bin', 'pip')
    pip = "%s %s -q install" % (remote_python, remote_pip)
    virtenv = "-E %s" % venv
    extra_idx = "--extra-index-url=http://opensource.washingtontimes.com/pypi/simple/"
    if version is None:
        pkg = package
    else:
        pkg = "%s==%s" % (package, version)
    cmd = [pip, virtenv, extra_idx, pkg]
    run(" ".join(cmd))
    if not env.updated_reqs:
        pkg_re = re.compile(r'%s\s*==\s*.+' % package)
        current_reqs = open('requirements.txt').read()
        if pkg_re.search(current_reqs):
            print "Updating %s entry to version %s in the requirements file..." % (package, version)
            new_reqs = pkg_re.sub(pkg, current_reqs)
        else:
            print "Adding %s entry in the requirements file..."
            new_reqs = current_reqs.strip('\n') + '\n' + pkg
        try:
            reqs_file = open('requirements.txt', 'w')
            reqs_file.write(new_reqs)
            set_env(updated_reqs = True)
        except IOError:
            print "Couldn't write to the requirements file."
    
        reqs_file.close()

def install_pkg_local(package, version):
    pip = "pip -q install"
    extra_idx = "--extra-index-url=http://opensource.washingtontimes.com/pypi/simple/"
    if version is None:
        pkg = package
    else:
        pkg = "%s==%s" % (package, version)
    cmd = [pip, extra_idx, pkg]
    local(" ".join(cmd))

def pkg_version(package):
    """
    Print out the version installed for a particular package
    """
    run("%sbin/pip freeze | grep %s" % (venv, package))


def update_reqs():
    """
    Have pip install the requirements file. This will update any dependencies
    that have changed in the requirements file.
    """
    req_path = os.path.join(site_path, 'setup', 'requirements.txt')
    run('%s/bin/pip install -E %s -r %s' % (venv, venv, req_path))

def reload():
    """
    Reload the apache process by touching the wsgi file
    """
    with cd(site_path):
        run('touch %s' % wsgi_path)

@hosts('webdev@172.16.12.92')
def sync_static_media():
    """
    Copies different static media files to the media server 
    from the local media directory
    """
    local_dir = os.path.abspath(os.path.join('..', 'media'))
    out = rsync_project(nfs_static_media_path, local_dir="%s/*" % local_dir, delete=True)
    print out

