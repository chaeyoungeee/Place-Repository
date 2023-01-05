
from flask import Flask, render_template, jsonify, request, session, url_for, redirect, flash
import pymysql
import requests
from bs4 import BeautifulSoup

conn = pymysql.connect(host='localhost', user='root', password='Duck9962@@',
                       db='place_repository', charset='utf8',  # 한글처리 (charset = 'utf8')
                       autocommit=True,  # 결과 DB 반영 (Insert or update)
                       cursorclass=pymysql.cursors.DictCursor  # DB조회시 컬럼명을 동시에 보여줌
                       )
cur = conn.cursor()

cur.execute('''
    select *
    from place
    where place_name in (select place_name from favorites where id='%s')
    ''' % ('12'))
data = cur.fetchall()
print(data)
cur.execute('''
select place_name from favorites where id='%s'
'''% ('12'))

data = cur.fetchall()
print(data)
conn.close()
