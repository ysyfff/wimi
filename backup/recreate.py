#!usr/bin/evn python
#coding:utf8

import sys, os
from django.core.management import setup_environ
from wim import settings
setup_environ(settings)

from wimi.settings import DATABASES
import MySQLdb

