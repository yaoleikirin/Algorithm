python -m pip install -i https://pypi.doubanio.com/simple/ --trusted-host pypi.doubanio.com datetime

max(x,y,z)  #取最大值
df : <class 'pandas.core.frame.DataFrame'>
df["close"] : <class 'pandas.core.series.Series'> 序列类，相当于取一列df.close 或 df["close"]
df["close"].rooling(10) <class 'pandas.core.window.rolling.Rolling'>  返回：Rolling [window=10,center=False,axis=0,method=single]
DataFrame.rolling(2) 滑窗为2
df["close"].rolling(10).mean() 平均数
df["close"].rooling(10).std()   标准差
df["close"].rooling(10).median() 中位数
var 方差 count 非np.nan的个数 min 最小值 max 最大值
#https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.core.window.rolling.Rolling.count.html
corr 两个列相关系数  v1 = [3, 3, 3, 5, 8] v2 = [3, 4, 4, 4, 8] s1 = pd.Series(v1) s2 = pd.Series(v2) s1.rolling(4).corr(s2)
cov(covariance)协方差
df["f10"] =False 对一整列赋值
df.loc['20130101','B'] = 2222 "20130101" index,"B" columns
df.loc[df['ts_code'] == symbol, 'namae'].values[0]
df.iloc[0:N,:]
target_symbols['symbol'] = target_symbols['ts_code'].map(lambda datai: datai.split('.')[1]+'SE.'+datai.split('.')[0])
# 展现统计结果
#https://github.com/xingbuxing/TA-Lib-in-chinese/blob/master/source/API/Pattern%20Recognition/CDL2CROWS.md
#https://github.com/mrjbq7/ta-lib/blob/master/talib/__init__.py
df.groupby(pattern_name)[[str(i)+'天后涨跌幅' for i in 1, 3, 5, 10]].describe()
list(range(2))=[0,1]

#log写入文件
import logging
xx="my name is Jim Green"
logging.basicConfig(level=logging.NOTSET, #NOTSET，全部级别都记录
                    filename='xx.log',
                    filemode='w',
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S'
                    )
logging.info(xx.encode('gbk').decode('gbk'))

import numpy as np
a=np.array([[1,2,4],[4,5,8],[4,9,2]])
# b=np.ones(2)
b=["1"]*3 #["你","你","你"]
np.insert(a, 0, values=b, axis=1) #沿Y轴插入到0列
df=df.append(df1, ignore_index=True)
#使用enumerate方法获得列表序号和元素
for index,item in enumerate(shee1_col):