#!/usr/bin/env python

from distutils.core import setup

setup(name='cherokee-admin-api',
      version='0.0.1',
      description='This python package can manipulate cherokee.conf',
      author='Yann Malet',
      author_email='yann.malet@gmail.com',
      packages=['cherokee_admin_api',],
      package_data={'cherokee_admin_api':['templates/configurations/*.conf.sample']},
     )