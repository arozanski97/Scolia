#!/usr/bin/env python3
import time
import os
from webserver.backend import db_util  
def f(file_path,JI):
	time.sleep(120)
	#db_util.delete_status(JI)
	command="rm -r "+file_path
	os.system(command)
