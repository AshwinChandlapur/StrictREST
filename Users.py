import app
from sqlalchemy import Column,String,Integer,Boolean

class User(app.db_sqlite.Model):
    __tablename__ = 'User'


    id = Column(Integer,primary_key=True)
    public_id = Column(String(50))
    name = Column(String(50))
    password = Column(String(50))
    admin = Column(Integer)