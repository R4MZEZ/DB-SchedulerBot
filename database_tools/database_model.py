from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DBConnection(object):
    def __init__(self, access_url):
        self.url = access_url
        self.engine = create_engine(access_url)
        self.Session = sessionmaker(autoflush=False, bind=self.engine)
        self.database = self.Session()
        self.connect = self.engine.connect()
