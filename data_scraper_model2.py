#scraping the stock price
import requests
from bs4 import BeautifulSoup
import datetime
#import pandas as pd
import os
import mysql.connector
import csv
r=requests.get('https://www.morningstar.com/markets')
html=r.content

soup=BeautifulSoup(html,'html.parser')
#all_data1=soup.find_all('div',{'class':'mdc-table-body mds-data-table__body'})
#print(soup.prettify())
#print(all_data1,'check-1')

#index = 0
csv_file=open('scraped_stock.csv','w')
csv_writer=csv.writer(csv_file)
csv_writer.writerow(['Product Name','Price','Date/Time'])

n_list=[]
p_list=[]
date=[]
conn=mysql.connector.connect(
            host='localhost',
            user=os.environ.get('USER'),
            passwd=os.environ.get('passwd'),
            database='stock'

            )
curr=conn.cursor()
#soup.find_all('td',{'mdc-table-cell mds-data-table__cell mdc-market-indexes-table__name mdc-table-cell--truncated'}))

def sto_price():
    global a
    global stock_name
    global stock_price
    global n_list
    global p_list
    global date


    for a in soup.find_all('td',{'class':'mdc-table-cell mds-data-table__cell mdc-table-link-cell mdc-market-indexes-table__name mdc-table-cell--truncated'}):

        stock_name = a.text
        n_list=n_list+[stock_name]
        date = date + [datetime.datetime.now()]

    for b in soup.find_all('td',{'class':'mdc-table-cell mds-data-table__cell mdc-table-link-cell mdc-market-indexes-table__price mds-data-table__cell--right'}):

        stock_price=b.text
        p_list=p_list+[stock_price]
    zipped = zip(n_list, p_list, date)
    e = list(zipped)
    print(e)
    csv_writer.writerows(e)
    csv_file.close()


def c_table():
    global a
    global stock_name
    global stock_price
    global n_list
    global p_list
    global date

    curr.execute("""DROP TABLE IF EXISTS data_table """)

    curr.execute("""

    CREATE TABLE data_table (
        stock_name text,
        stock_price text
    );

    """)

    conn.commit()

    for items in n_list:
        add_item = ("INSERT INTO data_table "
                    "(stock_name, stock_price) "
                    "VALUES (%s, %s)")

        data_item = (stock_name, stock_price)

        curr.execute(add_item, data_item)
        conn.commit()


sto_price()
c_table()




