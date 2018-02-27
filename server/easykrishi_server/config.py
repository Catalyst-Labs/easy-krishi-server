import os
import pdb
import pickle
import socket
#pdb.set_trace()
#fp = open("shared.obj","rb")
#shared = pickle.load(fp)
#DB_NAME = shared['DB_NAME']
#DB_USER = shared['DB_USER']
#DB_PASSWORD = shared['DB_PASSWORD']
#DB_HOST = shared['DB_HOST']
#fp.close()


DB_NAME='easykrishi'
DB_HOST='easykrishi_database'
DB_PASSWORD='easykrishi_pwd'
DB_USER= 'easykrishi'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': socket.gethostbyname(DB_HOST),
        # 'HOST': 'catalystdev.czxlxjwael6a.us-east-1.rds.amazonaws.com',
        'PORT': '3306',
        'OPTIONS': {
            #"init_command": "SET storage_engine=INNODB"
            #'ssl': {
            #            'ca': '/home/ubuntu/easykrishi/catalystlabs-server/server/easykrishi_server/rds-combined-ca-bundle.pem',
            #       },
            },
    }
}

