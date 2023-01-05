
from flask import Flask, render_template, jsonify, request, session, url_for, redirect, flash
import pymysql
import requests
from bs4 import BeautifulSoup

url = input()

conn = pymysql.connect(host='localhost', user='root', password='Duck9962@@',
                               db='place_repository', charset='utf8',  # 한글처리 (charset = 'utf8')
                               autocommit=True,  # 결과 DB 반영 (Insert or update)
                               cursorclass=pymysql.cursors.DictCursor  # DB조회시 컬럼명을 동시에 보여줌
                               )
cur = conn.cursor()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get(url, headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')

a = soup.find('div', {'class': 'YouOG'})
place_name = a.find('span', {'class': 'Fc1rA'}).text
type = a.find('span', {'class': 'DJJvD'}).text

b = soup.find('span', {'class': 'PXMot'})
rating = float(b.find('em').text)

location = soup.find('span', {'class': 'IH7VW'}).text

cur.execute("insert ignore into place values('%s', %f, '%s', '%s')" % (place_name, rating, location, type))

cur.execute("select * from place")
print(cur.fetchall())
conn.commit()
conn.close()