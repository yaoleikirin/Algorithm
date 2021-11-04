import pandas as pd
import time
import tushare as ts
import pymysql
from sqlalchemy import create_engine

start = time.time()
target_symbols = pd.DataFrame()
ts.set_token("6667cd4a2326f2f937062a0f4fb59aea5c56d13b1f6f26225f115fe9")
pro = ts.pro_api()
# data_1 = pro.stock_basic(exchange='', list_status='L', market="主板",fields='ts_code,name,area,industry,list_date')
data_1 = pro.stock_basic(exchange='', list_status='L', market="主板",fields='ts_code,name,area,industry,list_date') #'ts_code,name,area,industry,list_date')
data_2 = pro.stock_basic(exchange='', list_status='L', market="中小板",fields='ts_code,name,area,industry,list_date') #'ts_code,name,area,industry,list_date')  
target_symbols = data_1.append(data_2, ignore_index=True) 
# print(len(data_1),len(data_2))
# data=data_3.get('ts_code')
# out=data[0]
# out=out.split('.')
# out=out[1]+'SE.'+out[0]
# 把ts_code股票代码格式改成goldminer格式
# target_symbols=[datai.split('.')[1]+'SE.'+datai.split('.')[0] for datai in data]
target_symbols['symbol'] = target_symbols['ts_code'].map(lambda datai: datai.split('.')[1]+'SE.'+datai.split('.')[0])
# print(type(target_symbols))

DB_STRING = 'mysql+pymysql://root:kirin@localhost:3306/stock?charset=utf8'
engine = create_engine(DB_STRING)

"""
#执行太慢
ts_market=pd.DataFrame()
for i in data_1['ts_code']:
    try:
        ts_market=ts_market.append(pro.stock_basic(ts_code=i,fields="symbol,name,area,industry,list_date"), ignore_index=True)
    except:
        pass
"""
# df_ts_market = pd.DataFrame(target_symbols,columns=["symbol,name,area,industry,list_date"])
# cur.execute('SELECT * FROM ts_market')
# res= cur.fetchall()
# df_ts_market.to_sql("main_sme",engine,if_exists="replace",index=True)
target_symbols.to_sql("main_sme",engine,if_exists="replace",index=True)
print("执行时间 {} 秒".format(round(time.time() - start, 2)))

sql = ''' select * from main_sme; '''
# read_sql_query的两个参数: sql语句， 数据库连接
df = pd.read_sql_query(sql, engine)
# 输出employee表的查询结果
print(df)