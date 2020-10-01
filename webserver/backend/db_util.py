from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()
engine = create_engine('sqlite:///Scolia2.db', echo = True)
Session = sessionmaker(bind = engine)
session = Session()

class scolia_data(Base):

     __tablename__ = 'scolia_data'

     job_id = Column(Integer, primary_key=True)
     email = Column(String)
     job_submitted = Column(Integer)
     email_sent = Column(Integer)
     pipeline_number = Column(Integer)


def init_db():
    print("initialising db")
    Base.metadata.create_all(engine)


def insert(obj):
    session.add(obj)
    session.commit()

def update_pipeline_status(JI):
    print("in updated pipeline")
    #session.query(Customers).filter(Customers.id! = 2). update({Customers.name:"Mr."+Customers.name}, synchronize_session = False)
    #.update(dict(email='my_new_email@example.com'))
    row=session.query(scolia_data).get(JI)
    row.job_submitted = 1
    #print(xjob_submitted)
    #x.job_submitted=1
    #print(x.job_submitted)
    session.commit()

def get_one(JI):
    row = session.query(scolia_data).get(JI)
    return row

def get_job_id_for_emails():
    print("in get id for emails")
    results = session.query(scolia_data).filter(scolia_data.job_submitted == 1, scolia_data.email_sent == 0)
    required_ids = {}
    for result in results:
        required_ids[result.job_id] = (result.email)
    #print(required_ids)
    return (required_ids)


def update_email_status(JI, email_status):
    row=session.query(scolia_data).get(JI)
    row.email_sent = email_status
    session.commit()

def delete_status(JI):
    session.query(scoial_data).get(JI).delete()
    session.commit()
	
def clean_db():
    session.query(scolia_data).delete()
