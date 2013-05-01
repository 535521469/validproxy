# encoding:utf8
'''
Created on 2013-4-24
@author: corleone
'''
from bot.config import configdata
from bot.const import FetchConst, HTTPProxyValueConst
from bot.dbitem import HTTPProxy
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
import datetime

dbconfig = configdata[FetchConst.DBConfig]
# mysql://root:@localhost:3306/test
db_connect_str = (u'mysql+mysqldb://%s:%s@%s:%s/%s?charset='
                  '%s') % (dbconfig[FetchConst.DBConfig_user],
                           dbconfig[FetchConst.DBConfig_passwd],
                           dbconfig[FetchConst.DBConfig_host],
                           dbconfig[FetchConst.DBConfig_port],
                           dbconfig[FetchConst.DBConfig_dbname],
                           dbconfig[FetchConst.DBConfig_charactset],
                           )
                  
engine = create_engine(db_connect_str, echo=False,
                       pool_size=dbconfig.get(FetchConst.DBConfig_poolsize, 2))
FetchSession = sessionmaker(bind=engine)

def get_proxies(proxy_ids=None, d=None):
    fs = FetchSession()
    try:
        status = [HTTPProxyValueConst.validflag_yes,
                  HTTPProxyValueConst.validflag_null, ]
        proxies = fs.query(HTTPProxy).filter(HTTPProxy.validflag.in_(status))
        if proxy_ids:
            proxies = proxies.filter(HTTPProxy.seqid.in_(proxy_ids))
        if d:
            proxies = proxies.filter(HTTPProxy.fetchdate == d)
        proxies = proxies.all()
        return proxies
    except Exception as e:
        print str(e)
        fs.rollback()
        raise e
    else:
        fs.commit()
    finally:
        fs.close()
        
        
