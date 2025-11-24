"""Server configuration"""
import logging
import sys
from os import environ

DB_NAME = 'default'
DB_USER = 'default'
DB_PASSWORD = 'password'
DB_HOST = 'localhost'

HEADERS = {'Content-Type': 'application/json'}
TOKEN = {'bearer': 'xxx-xx-xxxxxx'}

api_key = environ.get('API_KEY') or 'test-api-key'
log_level = logging.INFO
port = 8080

if sys.platform == 'win32':
    num_workers = 10
else:
    num_workers = 100

# Clean up namespace
del __doc__
del environ
del logging
del sys
