# -*- coding: utf-8-*-
'''
python -m pip install -i https://pypi.doubanio.com/simple/ --trusted-host pypi.doubanio.com numpy
'''
#抓取网易的股票信息，股票名字、代码、所属行业
import urllib3
from bs4 import BeautifulSoup
# import html5lib
# import requests
# import json
# import sys
# import os
import time
import numpy as np
import pandas as pd

Today=time.strftime("%Y-%m-%d-%H-%M-%S")

class getstock:
    def __init__(self,count):
        self.data_h= ['date','open','high','low','close','change','pct_chg','hands','amount(w)','amp(%)','turnover(%)']   
        #['日期','开盘价', '最高价', '最低价', '收盘价', '涨跌额', '涨跌幅(%)', '成交量(手)', '成交金额(万元)', '振幅(%)', '换手率(%)']   
        self.count= str(count).zfill(6)
        if int(count) >= 600000:
            self.symbol = str(count).zfill(7)  
        else:             
            self.symbol = '1' + str(count).zfill(6)  
        #拼接Url
        self.url = 'http://quotes.money.163.com/'+self.symbol+'.html'
        soup=self.parse(self.url)
        #parse返回0，表示请求失败
        if  soup is None:
            print("解析失败!")
        stockinfo=soup.select('script')[4].contents[0].output_ready()  #{'window.stock_info':'price'})
        self.name=stockinfo.split(',')[0].split("'")[1]
        self.code=stockinfo.split(',')[1].split("'")[1]
        self.price=stockinfo.split(',')[2].split("'")[1]
        self.change = stockinfo.split(',')[3].split("'")[1].split("%")[0]
        self.pre_close = stockinfo.split(',')[4].split("'")[1]    
        self.open = stockinfo.split(',')[5].split("'")[1]      
        self.high = stockinfo.split(',')[6].split("'")[1]      
        self.low = stockinfo.split(',')[7].split("'")[1]  
        self.date = soup.find('table', {'class': 'divide_table'}).select('td')[1].next.split(" ")[0]
        self.high52w=soup.find('span', {'class': 'cRed'}).contents[0].output_ready()
        self.low52w = soup.find('span', {'class': 'cGreen'}).contents[0].output_ready()        
        self.dic={'name':self.name,'code':self.code,'price':self.price,'change':self.change,\
        'pre_close':self.pre_close,'open':self.open,'high':self.high,'low':self.low,'date':self.date,'high52w':self.high52w,'low52w':self.low52w}
    
    def parse(self,url,SoupStrainer=None):
        """parse url
        """
        http = urllib3.PoolManager()
        headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36"}
        response = http.request( 'get',url, headers= headers)
        if response.status==200:
          #status 参考 https://blog.csdn.net/Gjc_csdn/article/details/80449996
          # content = urllib3.urlopen(response).read()
            content =response.data
        else:
            print('response.status=',response.status)
            return 0
        parsers=['html.parser','lxml','xml','html5lib']
        soup = BeautifulSoup(content,parsers[3]) #parse_only=SoupStrainer)         
        return soup         

    def _season(self, year, season):
        #历史数据都是不复权的，当时交易价格
        self.url_history='http://quotes.money.163.com/trade/lsjysj_'+\
             self.count+'.html?year='+str(year)+'&season='+str(season)
        # print('_season url_history:',self.url_history)       
        soup1 = self.parse(self.url_history) #,only_table)      
        try:
           # method3  table class ="table_bg001 border_box limit_sale"
            cls_table=soup1.find_all(class_='table_bg001')
           # print(cls_table)        
            cls_table_cnt=cls_table[0].contents # cls_table_cnt=class table content历史数据表格
            head_data=cls_table_cnt[1]
            cur_data=cls_table_cnt[3]
            data_c=[] #包含所有数据，含日期           
            for string in  cur_data.strings:#耗时久,可以优化
                #print(repr(string))
                if string.strip():
                    data_c.append(string.replace(',', ''))   
            nn=np.asarray(data_c).reshape(len(data_c)//11,11)
            df = pd.DataFrame(nn, dtype='str', columns=self.data_h)
            df.replace("--",0,inplace=True)
            # df[['日期']]=df[['日期']].astype(str)
            df[['open','high','low','close','change','pct_chg','hands','amount(w)','amp(%)','turnover(%)']]=\
            df[['open','high','low','close','change','pct_chg','hands','amount(w)','amp(%)','turnover(%)']].astype(float)
            # print(type(df.iloc[0,0]),df.iloc[0,0])
            return df
        except Exception as errore:#这样出现错误继续执行
            print('when execute _season of', year,season,'occur:',errore)
            return 0  

    def dayN(self,N):
        curyear,curmonth,curday,hour,minute,second=Today.split('-')
        curseason=int(curmonth)//4+1
        df=self._season(int(curyear),curseason)
        return df.iloc[0:N,:]

    def history(self): #change name to history
        print("发行日期:",self.date) 
        styear,stmonth,stday=self.date.split('-')
        stseason=int(stmonth)//4+1
        curyear,curmonth,curday,hour,minute,second=Today.split('-')
        curseason=int(curmonth)//4+1
        year=int(curyear)
        season=int(curseason)        
        seasons=(int(curyear)-int(styear))*4+(curseason-stseason)
        df=self._season(year,season)
        seasons-=1
        season-=1
        while seasons>=0 :  
            if(season==0):
                season=4
                year-=1               
            df1=self._season(year,season)
            df=df.append(df1, ignore_index=True)   
            # print(df)  
            seasons-=1
            season-=1        
        print ('history execute ok')
        return df

    def lastN_ok(self,N): ##self必加
        count=self.count             
        year=Today.split('-')[0]
        season= int(Today.split('-')[1])//4+1
        df=self._season(year,season)
        open=df['open'][0:N]
        close=df['close'][0:N]
        high=df['high'][0:N]
        low=df['low'][0:N]
        for i in range (N):
            if ((low[i]/close[i]<0.98) and (low[i]/open[i] <0.98)):                  
                print ('target=',count)
                return 1 #success
    
    def rsi_n(self, n) :
        """
        #rsi=100*(sumn_rise) /(sumn_down+sumn_rise)
        """
        count=self.count
        #count stock code
        #n n days         
        df=self.history()
        wave=df['change']
        date=df['date']
        rsi=[]
        for i in range(len(wave)):
            npi=wave[i-n:i]
            if i<n :
                rsi.append(0)
            else:                
                sumn_rise=np.sum(npi[npi>0]) 
                sumn_down=np.sum(npi[npi<0])
                rsi.append(100*sumn_rise/(sumn_rise-sumn_down))
        rtn=[rsi[::-1],date[::-1]]             
        return rtn 
    def broadcast(self,str1):
        # import pyttsx3
        # pyttsx3.speak(str1)
        from gtts import gTTS 
        tts = gTTS(str1) 
        # tts.save('hello.mp3')
        
while("09:30:00"<time.strftime("%H:%M:%S", time.localtime())<"11:30:00" or "13:00:00"<time.strftime("%H:%M:%S", time.localtime())<"15:00:00"):  
    gs=getstock(600691)
    gs.broadcast(gs.price)
    time.sleep(30)
# print(gs.name,"开盘价:",gs.open)
# print(gs._season('2021','1'))
# print(gs.dayN(7))
# gs.lastN_ok(3)
# print(gs.rsi_n(6))
# print(gs.history())
#print(gs.parse.__doc__)
