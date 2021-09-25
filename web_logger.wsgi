#! /usr/bin/python3.6
import sys
import logging
import os

logging.basicConfig(format='%(asctime)s %(message)s', filename='stats.okewoke.com.log', level=logging.DEBUG)
os.chdir("/var/www/web_logger")
sys.path.insert(0,"/var/www/web_logger/")

from web_logger import app as application
application.secret_key = 'Add your secret key'
