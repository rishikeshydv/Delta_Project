#stock price
import requests
from bs4 import BeautifulSoup
import datetime
#import pandas as pd
import os
import mysql.connector
import csv
#import re

r=requests.get('https://robinhood.com/collections/technology')
html=r.content

soup=BeautifulSoup(html,'html.parser')
#print(soup.prettify())
#all_data1=soup.find_all('table',{'class':'_25eGUhpRN5n6jaWqzmSOZl'})

csv_file=open('data_scraper_model1.csv','w')
csv_writer=csv.writer(csv_file)
csv_writer.writerow(['Product Name','Price','Date/Time'])

name_list = []
price_list = []
dttm = []




conn=mysql.connector.connect(
        host='localhost',
        user=os.environ.get('USER'),
        passwd=os.environ.get('passwd'),
        database='my_data'

            )
curr=conn.cursor()

def websc():
    global name
    global a_price
    global name_list
    global price_list
    global dttm
    # print(all_data1, 'check 2')
    for n in soup.find_all('span',{'class':'_2fMBL180hIqVoxOuNVJgST'})[:]:


        name=n.text
        name_list = name_list + [name]
        dttm = dttm + [datetime.datetime.now()]
        #print(name_list)

    for p in soup.find_all('a',{'class':'rh-hyperlink'})[4::+6]:

        a_price = p.text
        price_list = price_list + [a_price]
        #print(price_list)
    zipped = zip(name_list, price_list,dttm)
    d = list(zipped)
    print(d)
    csv_writer.writerows(d)
    csv_file.close()



def create_table():

    global name
    global a_price
    global name_list
    global price_list
    global dttm




    curr.execute("""DROP TABLE IF EXISTS data_table """)

    curr.execute("""
    
    CREATE TABLE data_table (
        name text,
        a_price text
    );
    
    """)

    conn.commit()

    for items in name_list:

        add_item = ("INSERT INTO data_table "
                    "(name, a_price) "
                    "VALUES (%s, %s)")

        data_item = (name , a_price)

        curr.execute(add_item, data_item)
        conn.commit()


websc()
create_table()




