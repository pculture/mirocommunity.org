#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='mirocommunity.org',
      version='2.0',
      description='The main site for Miro Community.',
      maintainer='Participatory Culture Foundation',
      maintainer_email='dev@mirocommunity.org',
      url='http://www.mirocommunity.org/',
      packages=find_packages(),
      include_package_data=True,
      classifiers=[
          'Environment :: Web Environment',
          'Framework :: Django',
          'Intended Audience :: Developers',
          'Intended Audience :: System Administrators',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Topic :: Multimedia :: Sound/Audio',
          'Topic :: Multimedia :: Video',
      ],
      platforms=['OS Independent'],)
