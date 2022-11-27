from flask import Flask, render_template, jsonify, request, session, url_for, redirect, flash
import pymysql
import requests
from bs4 import BeautifulSoup

user_id = ''
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        id = request.form['id']
        global user_id
        user_id = id
        pw = request.form['password']

        conn = pymysql.connect(host='localhost', user='root', password='pw_',
                               db='place_repository', charset='utf8',  # 한글처리 (charset = 'utf8')
                               autocommit=True,  # 결과 DB 반영 (Insert or update)
                               cursorclass=pymysql.cursors.DictCursor  # DB조회시 컬럼명을 동시에 보여줌
                               )
        cur = conn.cursor()
        cur.execute("select * from user where id=%s and password=%s", (id, pw))
        account = cur.fetchone()
        conn.close()

        if account:
            session['logged_in'] = True
            return redirect(url_for('saving'))
        else:
            return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        id_ = request.form['id']
        pw_ = request.form['password']

        conn = pymysql.connect(host='localhost', user='root', password='pw_',
                               db='place_repository', charset='utf8',  # 한글처리 (charset = 'utf8')
                               autocommit=True,  # 결과 DB 반영 (Insert or update)
                               cursorclass=pymysql.cursors.DictCursor  # DB조회시 컬럼명을 동시에 보여줌
                               )
        cur = conn.cursor()
        cur.execute("insert into user values('%s', '%s')"%(id_, pw_))
        data = cur.fetchall()
        if not data:
            conn.commit()
            return render_template('login.html')
        else:
            conn.rollback()
            return "가입에 실패하였습니다."
        cur.close()
        conn.close()
    return render_template('register.html')


@app.route('/saving', methods=['GET', 'POST'])
def saving():
    if request.method == 'GET':
        return render_template('saving.html')
    else:
        conn = pymysql.connect(host='localhost', user='root', password='pw_',
                               db='place_repository', charset='utf8',  # 한글처리 (charset = 'utf8')
                               autocommit=True,  # 결과 DB 반영 (Insert or update)
                               cursorclass=pymysql.cursors.DictCursor  # DB조회시 컬럼명을 동시에 보여줌
                               )
        cur = conn.cursor()
        url = request.form['url']
        user_rating = float(request.form['user_rating'])
        comment = request.form['comment']


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

        cur.execute("insert ignore into place values('%s', %f, '%s', '%s')"%(place_name, rating, location, type))
        cur.execute("insert into place_comment values('%s', '%s', %f, '%s') on duplicate key update comment='%s'"%(user_id, place_name, user_rating, comment, comment))

        conn.commit()
        conn.close()
        return redirect(url_for('saving'))


@app.route('/storage', methods=['GET'])
def listing():
    conn = pymysql.connect(host='localhost', user='root', password='pw_',
                           db='place_repository', charset='utf8',  # 한글처리 (charset = 'utf8')
                           autocommit=True,  # 결과 DB 반영 (Insert or update)
                           cursorclass=pymysql.cursors.DictCursor  # DB조회시 컬럼명을 동시에 보여줌
                           )
    cur = conn.cursor()
    cur.execute('''
    select p.place_name, user_rating, type, comment
    from place as p
    inner join place_comment as pc
    on p.place_name in (select place_name from place_comment where id='%s') and p.place_name = pc.place_name
    '''%(user_id))
    data = cur.fetchall()
    new_data = []
    for i in range(len(data)):
        new_data.append(list(data[i].values()))
    conn.close()
    return render_template('storage.html', result=new_data)

@app.route('/recommend', methods=['GET', 'POST'])
def recommending():
    if request.method == 'GET':
        conn = pymysql.connect(host='localhost', user='root', password='pw_',
                               db='place_repository', charset='utf8',
                               autocommit=True,
                               cursorclass=pymysql.cursors.DictCursor)
        cur = conn.cursor()
        cur.execute('''
        select distinct type
        from place
        ''')
        data = cur.fetchall()
        conn.close()
        return render_template('selecting.html', result=data)
    else:
        type = request.form['type']
        conn = pymysql.connect(host='localhost', user='root', password='pw_',
                               db='place_repository', charset='utf8',  # 한글처리 (charset = 'utf8')
                               autocommit=True,  # 결과 DB 반영 (Insert or update)
                               cursorclass=pymysql.cursors.DictCursor  # DB조회시 컬럼명을 동시에 보여줌
                               )
        cur = conn.cursor()
        if type=='전체보기':
            cur.execute('''
                    select *
                    from place
                    order by rating desc
                    ''')
        else:
            cur.execute('''
            select *
            from place
            where type='%s'
            order by rating desc
            ''' % (type))
        data = cur.fetchall()
        conn.close()

        return render_template('recommending.html', result=data)
    
@app.route('/recommend_f', methods=['GET', 'POST'])
def add_favorites():
    if request.method == 'GET':
        return render_template('recommending.html')
    else:
        place_name = (request.form['place_name'])[3:-2]
        conn = pymysql.connect(host='localhost', user='root', password='pw_',
                            db='place_repository', charset='utf8',  # 한글처리 (charset = 'utf8')
                            autocommit=True,  # 결과 DB 반영 (Insert or update)
                            cursorclass=pymysql.cursors.DictCursor  # DB조회시 컬럼명을 동시에 보여줌
                            )
        cur = conn.cursor()
        cur.execute("insert ignore into favorites values('%s', '%s')"%(user_id, place_name))
        conn.commit()
        conn.close()
        
        return redirect(url_for('favorites'))
    
    

@app.route('/favorites', methods=['GET'])
def favorites():

    conn = pymysql.connect(host='localhost', user='root', password='pw_',
                           db='place_repository', charset='utf8',  # 한글처리 (charset = 'utf8')
                           autocommit=True,  # 결과 DB 반영 (Insert or update)
                           cursorclass=pymysql.cursors.DictCursor  # DB조회시 컬럼명을 동시에 보여줌
                           )
    cur = conn.cursor()

    cur.execute('''
    select *
    from place
    where place_name in (select place_name from favorites where id='%s')
    '''%(user_id))

    data = cur.fetchall()
    conn.close()

    return render_template('favorites.html', result=data)


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run('0.0.0.0', port=4900, debug=True)

