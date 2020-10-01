#!/usr/bin/env python3

import time
import os 
from webserver.backend import db_util
def f(x, input_dir, flag,output_dir):
    for i in range(0,x):
        print(i)
        time.sleep(1)
    print("JOBID :::::::::::::::::::::::::::::::::::::::::::"+input_dir.split('/')[-2])
    #db_util.update_pipeline_status(input_dir.split('/')[-2])
    #print(input_dir.split('/')[-2])
    if flag == 0:
        db_util.update_pipeline_status(input_dir.split('/')[-2])
        print("done")
        output_file=open(output_dir,"w+")
        output_file.close()	
        command="rm -r "+input_dir
        os.system(command)
