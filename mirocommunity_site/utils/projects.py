"""Tools for project creation."""

import logging
import os
import subprocess
import sys

from django.conf import settings
from django.core.management import call_command

from mirocommunity_site.utils.shell import check_output


def _project_name(site_name):
    return '{0}_project'.format(site_name.replace('-', '_'))


def create_project(site_name):
    """
    :param site_name: The name of the site to be created. It will be created
                      within ``settings.SITE_CREATION_ROOT``.

    Any additional keyword arguments will be passed to the startproject
    command and enter the template context.

    """
    project_root = settings.SITE_CREATION_ROOT
    project_name = _project_name(site_name)
    project_dir = os.path.join(project_root, project_name)
    if os.path.exists(project_dir):
        logging.error("{0} already exists in {1}".format(project_name,
                                                         project_root))
        raise ValueError
    os.mkdir(project_dir)

    options = {}
    template_path = getattr(settings, 'SITE_CREATION_TEMPLATE', None)
    if template_path is not None:
        options['template'] = template_path

    call_command('startproject', project_name, project_dir, **options)


def _mysql_database_name(site_name):
    """
    Given a site name, returns a database name for that site.

    """
    namespace = getattr(settings, 'PROJECT_NAMESPACE', '')
    prefix = '{0}_'.format(namespace) if namespace else ''
    return '{prefix}miro_community_{site_name}'.format(
                    prefix=prefix, site_name=site_name)


def create_mysql_database(database_name):
    """
    :param database_name: The name of the database being created.

    """
    cmdline = ['mysql']
    default_db = settings.DATABASES['default']
    for opt, setting in (
        ('--host', 'HOST'),
        ('--port', 'PORT'),
        ('--user', 'USER'),
        ('--password', 'PASSWORD')):
        val = default_db.get(setting)
        if val:
            cmdline.append('{0}={1}'.format(opt, val))
    cmdline.extend(['-e', 'CREATE DATABASE '
                    '`{0}`'.format(database_name)])
    subprocess.check_call(cmdline)


def syncdb(site_name):
    sys.path.insert(0, settings.SITE_CREATION_ROOT)
    project_name = _project_name(site_name)
    project_settings = __import__('{0}.settings'.format(
                                                    project_name)).settings
    del sys.path[0]

    python = getattr(settings, 'SITE_CREATION_PYTHON', '')
    django_admin = getattr(settings, 'SITE_CREATION_DJANGO_ADMIN', '')
    if python and django_admin:
        cmdline = [python, django_admin]
    else:
        cmdline = ['django-admin.py']

    cmdline.extend(['syncdb',
                    '--settings={0}.settings'.format(project_name),
                    '--noinput'])
    if 'south' in project_settings.INSTALLED_APPS:
        cmdline.append('--all')

    env = os.environ.copy()
    env['PYTHONPATH'] = settings.SITE_CREATION_ROOT
    subprocess.check_call(cmdline, env=env)


def initialize(site_name, username='', email='', password='',
               tier='basic'):
    settings_module = '{0}.settings'.format(_project_name(site_name))

    python = getattr(settings, 'SITE_CREATION_PYTHON', '')
    django_admin = getattr(settings, 'SITE_CREATION_DJANGO_ADMIN', '')
    if python and django_admin:
        cmdline = [python, django_admin]
    else:
        cmdline = ['django-admin.py']

    cmdline.extend(['initialize',
                    site_name,
                    '--settings={0}'.format(settings_module),
                    '--tier={0}'.format(tier)])
    if username:
        cmdline.extend(['--username={0}'.format(username),
                        '--email={0}'.format(email),
                        '--password={0}'.format(password)])
    env = os.environ.copy()
    env['PYTHONPATH'] = settings.SITE_CREATION_ROOT
    output = check_output(cmdline, env=env)
    return output.rsplit('\n', 1)[1]
