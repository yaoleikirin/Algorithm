"""最小二乘法"""
import numpy as np
import datetime
from stockSelect10_soup_phone import getstock
# import matplotlib.pyplot as plt
#https://zhuanlan.zhihu.com/p/38128785/

def fun2ploy(x,n):  #得到范德蒙德（Vandermonde）行列式
    '''
    数据转化为[x^0,x^1,x^2,...x^n]
    首列变1
    '''
    lens = len(x)
    X = np.ones([1,lens])
    for i in range(1,n):
        X = np.vstack((X,np.power(x,i)))#按行堆叠
    return X  

def leastseq_byploy(x,y,ploy_dim):  #https://blog.csdn.net/dz4543/article/details/85224391
    '''
    最小二乘求解
    '''
    X = fun2ploy(x,ploy_dim)
    #直接求解
    Xt = X.transpose();#转置变成列向量 X=[[x^0][x^1][x^2][x^3]]
    XXt=X.dot(Xt);#矩阵乘,X*X^T
    XXtInv = np.linalg.inv(XXt)#求逆 (X*X^T)^-1
    XXtInvX = XXtInv.dot(X) #(X*X^T)^-1*X
    coef = XXtInvX.dot(y.T)
    y_est = Xt.dot(coef)
    return y_est,coef

def fit_func(p, x):  ## 如 p=numpy.poly1d([1,2,3])  生成  $1x^2+2x^1+3x^0$*,coef 傅立叶展开
    p=p[::-1]
    f = np.poly1d(p)
    return f(x)

# 最小二乘拟合
#https://www.cnblogs.com/lc1217/p/6514734.html

symbols=['2108','2600','2146','2938','2269'] #[沧州明珠,领益制造,荣盛发展,鹏鼎控股,美邦服饰]
for i in symbols:
    ploy_dim=2
    gs=getstock(i)
    days=7
    df7=gs.dayN(days)
    Yh=df7["high"].values
    Yl=df7["low"].values
    Xo=df7["open"].values
    [h_est,h_coef] = leastseq_byploy(Xo,Yh,ploy_dim)
    [l_est,l_coef] = leastseq_byploy(Xo,Yl,ploy_dim)
    # org_data_h = plt.scatter(Xo,Yh,color="red",marker='o',s = 50)
    # org_data_l = plt.scatter(Xo,Yl,color="green",marker='o',s = 50)
    # h_est_data = plt.scatter(Xo,h_est,color="pink",linewidth= 2)
    # l_est_data = plt.scatter(Xo,l_est,color="grey",linewidth= 2)
    # plt.show()
    #https://baike.baidu.com/item/黑塞矩阵/2248782?fr=aladdin
    xo1=float(gs.open)
    print(gs.name)
    print("预估最高价:",fit_func(h_coef,xo1))
    print("预估最低价:",fit_func(l_coef,xo1))