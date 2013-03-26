#!usr/bin/evn python
#coding:utf8

import os
from django.core.management import setup_environ
from wimi import settings
setup_environ(settings)

from wimi.settings import DATABASES
import MySQLdb

from backup.create_user import *
from backup.create_store import *


def clean_database():
    db = DATABASES['default']
    con = MySQLdb.connect(host=db['HOST'],
        user=db['USER'], passwd=db['PASSWORD'])
    name = db['NAME']
    print name
    try:
        con.query('drop database ' + name)
    except:
        pass
    con.query('create database ' + name + ' character set utf8')
    con.commit()
    os.system('echo "no"|./manage.py syncdb')


def insert_db():
    insert_user()
    insert_store()
    insert_food()


if __name__ == '__main__':
    clean_database()
    insert_db()
