"""Tools for project creation."""

import logging
import os
import shutil
import subprocess
import sys

from django.conf import settings
from django.core.management import call_command

from mirocommunity_site.utils.shell import check_output


def _project_name(site_name):
    return '{0}_project'.format(site_name.replace('-', '_'))


def _site_domain(site_name):
    namespace = getattr(settings, 'SITE_CREATION_NAMESPACE', '')
    return "{site_name}.{namespace}{dot}mirocommunity.org".format(
                            site_name=site_name, namespace=namespace,
                            dot='.' if namespace else '')


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

    template_path = getattr(settings, 'SITE_CREATION_TEMPLATE', None)

    if template_path is None:
        os.mkdir(project_dir)
        call_command('startproject', project_name, project_dir)
    else:
        shutil.copytree(settings.SITE_CREATION_TEMPLATE,
                        project_dir,
                        symlinks=True)


def _mysql_database_name(site_name):
    """
    Given a site name, returns a database name for that site.

    """
    namespace = getattr(settings, 'SITE_CREATION_NAMESPACE', '')
    prefix = '{0}_'.format(namespace) if namespace else ''
    return '{prefix}miro_community_{site_name}'.format(
                    prefix=prefix, site_name=site_name.replace('-', '_'))


def _run_mysql_command(command, **kwargs):
    """
    Runs the given MySQL command with the current server.
    """
    cmdline = ['mysql']
    default_db = settings.DATABASES['default']
    options = {}
    for setting in ('HOST', 'PORT', 'USER', 'PASSWORD'):
        val = default_db.get(setting)
        if val:
            options[setting.lower()] = val
    options.update(kwargs)
    for opt, val in options.iteritems():
        cmdline.append('--{0}={1}'.format(opt, val))
    cmdline.extend(['-e', command])
    subprocess.check_call(cmdline)


def create_mysql_database(database_name):
    """
    :param database_name: The name of the database being created.

    """
    _run_mysql_command('CREATE DATABASE `{0}`'
                       'COLLATE utf8_general_ci'.format(database_name))


def syncdb(site_name):
    syncdb_sql = getattr(settings, 'SITE_CREATION_SYNCDB_SQL', '')
    if syncdb_sql:
        if (settings.DATABASES['default']['ENGINE'] ==
            'django.db.backends.mysql'):
            _run_mysql_command('SOURCE {0}'.format(syncdb_sql),
                               database=_mysql_database_name(site_name))
            return
        else:
            raise ValueError("Unhandled database for sql import.")
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
                    _site_domain(site_name),
                    '--settings={0}'.format(settings_module),
                    '--tier={0}'.format(tier)])
    if username:
        cmdline.extend(['--username={0}'.format(username),
                        '--email={0}'.format(email),
                        '--password={0}'.format(password)])
    env = os.environ.copy()
    env['PYTHONPATH'] = settings.SITE_CREATION_ROOT
    output = check_output(cmdline, env=env)
    return output.rsplit('\n', 1)[-1]
