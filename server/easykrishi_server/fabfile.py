from __future__ import with_statement,absolute_import
import pdb
from fab_deploy import *
from fabric.main import main
from fabric.api import *
import os
import posixpath
import pprint
from copy import deepcopy
from re import match
from functools import wraps
from fabric.api import env, prefix, cd, abort, warn, puts, run
from fabric.contrib import files
from fabric import state
from fabric import network
import pickle
import os

if not os.environ.get('DEV', False):
    env.hosts = ['ec2-54-144-105-167.compute-1.amazonaws.com']
else:    
    env.hosts = ['localhost']

env.key_filename = "/home/ubuntu/public.pem"
def deploy(user,password,db):
    shared = {"DB_NAME":db, "DB_USER":user,"DB_PASSWORD":password, "DB_HOST": 'easykrishi_database'}
    fp = open("shared.obj","wb")
    pickle.dump(shared, fp)
    fp.close()

    my_site(user,password,db)
    with cd('.'):
        #local('pkill gunicorn')
        local('python manage.py makemigrations')
        local('python manage.py migrate')
        local('gunicorn easykrishi.wsgi:application --bind=0.0.0.0:8000 --workers=4 ')

def my_site(user,password,db):    
    env.key_filename = "/home/ubuntu/public.pem"
    env.conf = dict(
            DB_USER = user,
            DB_PASSWORD = password,
            DB_NAME = db,
                        DB_HOST = 'easykrishi_database'
    )
    #update_env()
