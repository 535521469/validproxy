# encoding=utf8
'''
Created on 2013-4-24
@author: corleone
'''
from sqlalchemy.ext.declarative.api import declarative_base
from sqlalchemy.schema import Column
from sqlalchemy.types import String, DateTime, Date
from uuid import uuid4
gen_uuid = lambda :unicode(uuid4()).replace('-', u'')

Base = declarative_base()

class HTTPProxy(Base):
    
    __tablename__ = 'HTTPProxy'
    
    seqid = Column("SEQID", String, primary_key=True, default=gen_uuid)
    procotol = Column("Procotol", String,)
    ip = Column("IP", String,)
    port = Column("Port", String,)
    validdatetime = Column("ValidDateTime", DateTime,)
    validflag = Column("ValidFlag", String,)
    fetchdate = Column("FetchDate", Date,)

    
    
