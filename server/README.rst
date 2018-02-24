Catalyst Server
==============

Development
-----------

::

   $ virtualenv env 
   $ pip install cookiecutter 

Bootstrap the app using django cookiecutte. 

::

   $ cookiecutter https://github.com/pydanny/cookiecutter-django
   Cloning into 'cookiecutter-django'...
   remote: Counting objects: 550, done.
   remote: Compressing objects: 100% (310/310) 
   ....


* Change the db to sqlitedb for development. Dont do server-side development. It is only for test. 
* Use migrations alone See `tutorial <https://realpython.com/blog/python/django-migrations-a-primer/>`_

Deployment
-----------

Use `fabric <http://docs.fabfile.org/en/1.11/tutorial.html>`_ 

::

   # This command should be support 
   $ fab deploy test 
