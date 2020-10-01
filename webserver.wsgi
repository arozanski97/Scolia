#! /projects/VirtualHost/predictc/html/miniconda_webserver/envs/T3W/bin/python3.5
import logging
import sys
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/projects/VirtualHost/predictc/html')
from webserver import create_app
application = create_app()
application.secret_key = 'Team3WebServer'
application.run(host='130.207.66.119',debug=True,port=8081)
