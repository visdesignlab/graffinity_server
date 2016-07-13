#!/usr/bin/python
import sys
import os
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, "/var/www/connectivity_matrix_server")
os.chdir("/var/www/connectivity_matrix_server")
from connectivity_matrix_backend import app as application