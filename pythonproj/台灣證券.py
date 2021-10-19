import requests
import pandas as pd
from io import StringIO
import sqlite3
import time

conn = sqlite3.connect('台灣證券.db')

d1 = pd.date_range('20200901','20211018')

for dtemp in d1:
    d = str(dtemp)[:10].replace('-','')
    print(d)
    
    sql = 'Select * from 股票 where 日期 = "' + d + '"'
    try:
        dfcheck = pd.read_sql(sql, conn)
    except:
        dfcheck = pd.DataFrame()
        
    if len(dfcheck) == 0 :
        time.sleep(5)
        url = 'https://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date='+ d +'&type=ALLBUT0999'
        
        resp = requests.get(url)
        if resp.status_code == 200 and len(resp.text) != 0 :
        
            content = resp.text
                
            clist = content.split('\n')
            result = ''
            for i in clist:
                if len(i.split('",')) == 17:
                    result += i + '\n'
                    
            df = pd.read_csv( StringIO(result))
            df = df.iloc[:,:-1]
            
            for i in range(2,16):
                if (i != 9) and df.iloc[:,i].dtype == 'object' :
                    df.iloc[:,i] = df.iloc[:,i].str.replace(',','')
                    df.iloc[:,i] = pd.to_numeric(df.iloc[:,i], errors = 'coerce')
                    
            df.iloc[:,0] = df.iloc[:,0].str.replace('=','').str.replace('"','')
            
            df['日期'] = d
            df.to_sql('股票', conn, if_exists = 'append', index = False)





























