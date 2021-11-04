#https://www.cnblogs.com/lc1217/p/6514734.html
##最小二乘法
import numpy as np   ##科学计算库 
import scipy as sp   ##在numpy基础上实现的部分算法库

# import matplotlib.pyplot as plt  ##绘图库
# import matplotlib 
# from matplotlib.pylab import mpl  
# mpl.rcParams['font.sans-serif'] = ['FangSong'] # 指定默认字体  
# mpl.rcParams['axes.unicode_minus'] = False #  解决保存图像是负号'-'显示为方块的问题 


import tushare as ts
ts.set_token("6667cd4a2326f2f937062a0f4fb59aea5c56d13b1f6f26225f115fe9")
pro = ts.pro_api()
#查询当前所有正常上市交易的股票列表
import time 
start = time.time()
data_1 = pro.stock_basic(exchange='', list_status='L', market="主板",fields='ts_code') #'ts_  code,symbol,name,area,industry,list_date')
data_2 = pro.stock_basic(exchange='', list_status='L', market="中小板",fields='ts_code') #'ts_code,symbol,name,area,industry,list_date')  
data=data_1.append(data_2, ignore_index=True) 
print(len(data["ts_code"]))

ts_codes=[]

import datetime
today = datetime.date.today()
start_day=(today-datetime.timedelta(8)).strftime('%Y%m%d') #9日交易日(含休市)数据拟合

for ts_code in data_2["ts_code"]:
    try:
        df7 = pro.daily(ts_code=ts_code, start_date=start_day)
        change=df7['change'].values #数据日期从近到远
        change_bool=change<0
        # a=np.asarray([1,2,3,4,3,1])
        # b=np.diff(a)
        # c=b<0
        # print(c[:-2].all(),c[-2:].all())
        print(ts_code)
        # print(change_bool[2:],~change_bool[:2])
        if change_bool[2:].all() and (~change_bool[:2]).all():#之前一直跌,近两天回调
            ts_codes.append(ts_code)
            print(ts_code,"is ok!")
    except:
        pass
print(ts_codes)

import pandas as pd
ts_market=pd.DataFrame()
for i in ts_codes:
    try:
        ts_market=ts_market.append(pro.stock_basic(ts_code=i,fields="market,name,industry,area,list_date"), ignore_index=True)
    except:
        pass
print(ts_market)
ts_market.to_csv("./ts_market%s.csv"%today.strftime('%Y%m%d'))
print("执行时间 {} 秒".format(round(time.time() - start, 2)))