from flask import Flask
from webserver.backend import db_util
import time
from flask_mail import Mail, Message
from multiprocessing import Pool
#from webserver.backend import function
import multiprocessing

DOWNLOAD_URL_PATH = 'http://http://predict2020t3.biosci.gatech.edu/download?id=:id:'

def init_email_sender(mail_instance):
    print("::::::::::::::initialising email sender")

    p = multiprocessing.Process(target=f, args=(mail_instance,))
    p.start()

    #pool2 = Pool(processes=2)
    #pool2.apply_async(function.f,(10,"",0,))
    #pool2.join()
    #pool2.apply_async(function.f,(10,"",0,))
    #pool2.apply_async(background_email_sender,(mail_instance,))


def f(mail_instance):
    """
    for i in range(0,x):
        print(i)
        time.sleep(1)
    """
    while True:
        print("**********************while loop*************************")
        required_id = db_util.get_job_id_for_emails()
        print(required_id)

        for job_id,email in required_id.items():
            download_url = generate_download_url(job_id)
            send_email(download_url,email,mail_instance)
        time.sleep(10)

def generate_download_url(job_id):
    print("***************************")
    download_url = DOWNLOAD_URL_PATH.replace(':id:',str(job_id))

    return download_url

def send_email(download_url, email,mail_instance):
    if is_email_valid(email):
        msg = Message('Scolia Result', sender = 'scoliagatech@gmail.com', recipients=[email])
        msg.body = "Please click on the URL to download the results:" + "\n" + "\t"+ download_url
        mail_instance.send(msg)
        db_util.update_email_status(download_url.split('=')[1], 1)
    else:
        db_util.update_email_status(download_url.split('=')[1], -1)

def is_email_valid (email):
    if (email is None) or (not email):
        return False
    if (len(email.split('@')) != 2) or (email.index('@')<1) or (email.index('@')+2>email.rfind('.')) or (email.rfind('.')+2>len(email)):
        return False

    return True
