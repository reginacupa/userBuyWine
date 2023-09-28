from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
import os

from Model.Base import Base
from Model.Cliente import Cliente

db_path = 'database/'

if not os.path.exists(db_path):
    os.makedirs(db_path)

db_url = 'sqlite:///%s/db.sqlite3' % db_path

engine = create_engine(db_url, echo=False)

Session = sessionmaker(bind=engine)

if not database_exists(db_url):
    create_database(db_url)

Base.metadata.create_all(engine)