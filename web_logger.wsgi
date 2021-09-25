#! /usr/bin/python3.6
import sys
import logging
import os

logging.basicConfig(stream=sys.stderr)
os.chdir("/var/www/web_logger")
sys.path.insert(0,"/var/www/web_logger/")

from web_logger import app as application
application.secret_key = 'Add your secret key'
#application.root_path = "/var/www/flaskSite/flaskSite/"
