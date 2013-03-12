====================
cherokee admin api
====================

Project scope
==============

The Goal of this project is to provide an easy way to programmatically, in python, create and manipulate a cherokee.conf. Cherokee-admin give us a wonderful UI to interactively setup and configure a cherokee web server but it does not cover the use case where you need to automate repetitive tasks. I have decided to explore what it would take to create such package. Since cherokee-admin is written in python I have extracted the parser that is used to read and write cherokee.conf and added some functions to create:
   
• vserver
• source
• rule

Where to get it ?
==================

You can access the code on my bitbucket account [here http://bitbucket.org/yml/cherokee-admin-api]. It is not yet ready for production but I think it can give you an idea of what you could do with this kind of tool.

How to install it
==================

|   #!shell
|   mkdir test_cheroke_api
|   cd test_cheroke_api/
|   pip install -E ve -e hg+http://bitbucket.org/yml/cherokee-admin-api#egg=cherokee_admin_api
|   pip install -E ve -r ve/src/cherokee-admin-api/requirements.pip



In order to check that everything is working fine on your end you can run the test suite.

|    #!shell
|    nosetests -w tests/
|    .......
|    ----------------------------------------------------------------------
|    Ran 7 tests in 0.660s
|    OK

How to us it
=============

cherokee-admin-api comes with examples, `wsgi_conf_generator.py` configure
cherokee to serve a wsgi application using uwsgi.

|   #!shell
|   pip install -E ve -r ve/src/cherokee-admin-api/examples/requirements.pip
|   . ve/bin/activate
|   cd ve/src/cherokee-admin-api/examples/
|   python wsgi_conf_generator.py 
|   sudo cherokee -C wsgi-cherokee-gene.conf



This will confirm that you are all set and can now start to work with cherokee-admin-api.

