#-*-coding:utf-8 -*
import tushare as ts
from gm.api import *
import pymysql
from sqlalchemy import create_engine
import time 
import pandas as pd
import datetime
import target_symbols_to_sql
from chinese_calendar import is_holiday
import matplotlib

pro = ts.pro_api()
#tushare 密钥
ts.set_token("6667cd4a2326f2f937062a0f4fb59aea5c56d13b1f6f26225f115fe9")

#goldminer 密钥
set_token("2f6fc0b33f43707de870abf5b0c2f9bade9204f2")
start = time.time()
DB_STRING = 'mysql+pymysql://root:kirin@localhost:3306/stock?charset=utf8'
engine = create_engine(DB_STRING)
sql = ''' select ts_code,symbol from main_sme; '''
# read_sql_query的两个参数: sql语句， 数据库连接
df = pd.read_sql_query(sql, engine)
#数据量太大,时间太长,取消<循环更新7天数据>做法
# gm_market=pd.DataFrame()
# for i in df['ts_code'][0:40]:
#     try:
#         gm_market=gm_market.append(history_n(i, '1d', count=7, end_time=None, fields='symbol,open,close,high,low,eob', skip_suspended=True, \
#           fill_missing='Last', adjust=ADJUST_NONE, adjust_end_time='', df=True), ignore_index=True)
#     except:
#         pass

# # cur.execute('SELECT * FROM gm_market')
# # res= cur.fetchall()
# gm_market.to_sql("gm_canbuy_info_3113",engine,if_exists="replace",index=True)
# print(gm_market)
today = datetime.date.today()
while is_holiday(today):
    today=today-datetime.timedelta(1)

# start_day=(today-datetime.timedelta(8)).strftime('%Y%m%d') #9日交易日(含休市)数据拟合
symbols=df["ts_code"].tolist()
# gm_market=pd.DataFrame()
# for i in df['symbol'][0:2]:
#     try:
#         gm_market=gm_market.append(history(i, '1d', start_time=start_day, end_time=None, fields='symbol,open,close,high,low,eob', skip_suspended=True, \
#           fill_missing='Last', adjust=ADJUST_NONE, adjust_end_time='', df=True), ignore_index=True)
#     except:
#         pass
start_date=today.strftime('%Y%m%d')
# cur.execute('SELECT * FROM gm_market')
# res= cur.fetchall()
df1=pd.DataFrame()
"""
中间添加上面变量或函数的说明文字
"""
symbols_c_list=[]
#列表个数不能超过限制100个
for i in range(len(symbols)//100):   
    symbols_c= ""
    for j in symbols[i*100:i*100+99]:
        if symbols_c == "":
            symbols_c += j  
        else:
            symbols_c += "," + j
    symbols_c_list.append(symbols_c)
    df = pro.daily(ts_code=symbols_c, start_date=start_date, end_date=start_date) 
    df1 = df1.append(df, ignore_index=True) 

#剩余除以100的余数
symbols_c= ""
for j in symbols[i*100+100:]:
        if symbols_c == "":
            symbols_c += j  
        else:
            symbols_c += "," + j
symbols_c_list.append(symbols_c)
df = pro.daily(ts_code=symbols_c, start_date='20211029', end_date='20211029') 
df1 = df1.append(df, ignore_index=True) 

df1.to_sql("gm_canbuy_info_3113",engine,if_exists="replace",index=True)
print(df1)
print("执行时间 {} 秒".format(round(time.time() - start, 2)))
sql = ''' select ts_code,pct_chg from gm_canbuy_info_3113; ''' #ts_code,trade_date,open,high,low,close,pre_close,change,pct_chg,vol,amount
# read_sql_query的两个参数: sql语句， 数据库连接
df_sorted = pd.read_sql_query(sql, engine)
# df 排序例句：df.sort_values(by=['Name', 'Score'], ascending=False) #ascending=False表示降序
df_sorted=df_sorted.sort_values(by="pct_chg", ascending=False) 
df_sorted.to_csv("./主板按涨跌幅从高到低排序.csv")
print(df_sorted)




