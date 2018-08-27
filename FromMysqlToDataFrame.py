#從Mysql資料庫讀取台股資料放進DataFrame，進行分析
import pandas as pd
import datetime
import matplotlib.pyplot as pp
import pymysql
MYSQL_HOST = 'localhost'
MYSQL_DB = 'TwStock'
MYSQL_USER = 'root'
MYSQL_PASS = ''

def connect_mysql():  #連線資料庫
    global connect, cursor
    connect = pymysql.connect(host = MYSQL_HOST, db = MYSQL_DB, user = MYSQL_USER, password = MYSQL_PASS,
            charset = 'utf8', use_unicode = True)
    cursor = connect.cursor()

connect_mysql()
stock = pd.read_sql('SELECT * FROM twse order by date, stockno', con = connect) #使用連線connect執行指定的SQL獲取資料
#print(stock)
indexlist = []
for i in range(len(stock)):
    indexlist.append(stock['date'][i])  #stock['date'][i]為datetime.date物件
stock.index = indexlist  #索引值改成日期
stock = stock.drop(['date'],axis = 1)  #刪除日期欄位
mlist = []
for item in stock.index:
    mlist.append(item.month)
stock['month'] = mlist  #新增月份欄位
print(stock)
result = stock
for item in result[result.close > 21]:  #收盤價大於21元
    print(item)
    
print(result[(result.index >= datetime.date(2018, 6, 1)) & (result.index <= datetime.date(2018, 6, 30)) & (result.close >= 21)])  #六月份大於21元

tmp = result.sort_values(by = 'close', ascending=False)
print(tmp[:3])  #取收盤價前三高

print(result.loc[datetime.date(2018, 6, 1):datetime.date(2018, 6, 30)])  #只顯示2018六月份

print(result.loc[datetime.date(2018, 1, 1):datetime.date(2018, 12, 31)].groupby('month').close.count())  #2018每個月幾個營業日

print(result.loc[datetime.date(2018, 1, 1):datetime.date(2018, 12, 31)].groupby('month').shares.sum())  #每個月累計成交股數

result.loc[datetime.date(2018, 1, 1):datetime.date(2018, 12, 31)].groupby('month').shares.sum().plot()  #月累計成交股數圖
pp.ylabel('shares')
pp.title('month of shares')