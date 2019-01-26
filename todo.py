import app
from sqlalchemy import Column,String,Integer,Boolean

class todo(app.db_sqlite.Model):
    id = Column(Integer,primary_key=True)
    text = Column(String(50))
    complete = Column(Boolean)
    user_id = Column(Integer)