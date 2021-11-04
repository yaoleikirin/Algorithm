import time 
start = time.time()
import pymysql

from sqlalchemy import create_engine
DB_STRING = 'mysql+pymysql://root:123@localhost:3306/stock?charset=utf8'
engine = create_engine(DB_STRING)

from pandas.core.frame import DataFrame
import tushare as ts
ts.set_token("6667cd4a2326f2f937062a0f4fb59aea5c56d13b1f6f26225f115fe9")
pro = ts.pro_api()
# data_1 = pro.stock_basic(exchange='', list_status='L', market="主板",fields='ts_code,name,area,industry,list_date')
data_1 = pro.stock_basic(exchange='', list_status='L', market="主板",fields='ts_code,name,industry') #'ts_  code,symbol,name,area,industry,list_date')
data_2 = pro.stock_basic(exchange='', list_status='L', market="中小板",fields='ts_code,name,industry') #'ts_code,symbol,name,area,industry,list_date')  
data_3  = data_1.append(data_2, ignore_index=True) 
print(len(data_1),len(data_2))
data=data_3.get('ts_code')
# out=data[0]
# out=out.split('.')
# out=out[1]+'SE.'+out[0]
target_symbols=[datai.split('.')[1]+'SE.'+datai.split('.')[0] for datai in data]
target_dict={"ts_code":target_symbols,'name':data_3.get('name'),'industry':data_3.get('industry')}
target_symbols_df=DataFrame(target_dict)
print(target_symbols_df)

import pymysql
from sqlalchemy import create_engine
DB_STRING = 'mysql+pymysql://root:123@localhost:3306/stock?charset=utf8'
engine = create_engine(DB_STRING)
target_symbols_df.to_sql("gm_market_3113",engine,if_exists="replace",index=True)
print("执行时间 {} 秒".format(round(time.time() - start, 2)))