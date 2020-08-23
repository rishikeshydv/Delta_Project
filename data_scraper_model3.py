#scraping the reviews of the client on hotels/restraunts
import requests
from bs4 import BeautifulSoup
import pandas as pd
import mysql.connector
import os
import datetime
import csv
r=requests.get('https://www.tripadvisor.com/Tourism-g60763-New_York_City_New_York-Vacations')
html=r.content

soup=BeautifulSoup(html,'html.parser') 
#all_data1=soup.find_all('div',{'class':'ui_container'})
    

n_hotel=[]
rev=[]
d_t=[]
csv_file=open('reviews.csv','w')
csv_writer=csv.writer(csv_file)
csv_writer.writerow(['Firm Name','Review','Date/Time'])

conn=mysql.connector.connect(
            host='localhost',
            user=os.environ.get('USER'),
            passwd=os.environ.get('passwd'),
            database='client_reviews'
            
            )
curr=conn.cursor()

def review():
    global n_hotel
    global rev
    global d_t

    #global price_list
    #global dttm
    # print(all_data1, 'check 2')
    for x in soup.find_all('div',{'class':'_1BdZ1sPm gZ95jyA4 _38K76hiv'}):


        name=x.text
        n_hotel = n_hotel + [name]
        d_t = d_t + [datetime.datetime.now()]
        #print(name_list)

    for y in soup.find_all('span',{'class':'_1KK223I5'}):

        r = y.text
        rev = rev + [r]
        #print(price_list)
    zipped = zip(n_hotel, rev, d_t)
    d = list(zipped)
    print(d)
    csv_writer.writerows(d)
    csv_file.close()


def cr_table():
    global n_hotel
    global rev
    global d_t

    curr.execute("""DROP TABLE IF EXISTS data_table """)

    curr.execute("""
    CREATE TABLE data_table (
    name text,
    r text
    );

    """)

    conn.commit()

    for items in file:
        t_name = items['Firm Name']
        t_rev = items['Review']

        add_item = ("INSERT INTO data_table "
                    "(name, r) "
                    "VALUES (%s, %s)")
        data_item = (t_name, t_rev)
        cursor.execute(add_item, data_item)
        conn.commit()


review()
cr_table()




