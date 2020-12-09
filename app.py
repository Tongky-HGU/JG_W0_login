from flask import Flask, render_template, jsonify, request, session
from pymongo import MongoClient
import requests

app = Flask(__name__)

client = MongoClient('mongodb://test:test@localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.session  # 'dbsparta'라는 이름의 db를 만들거나 사용합니다.


@app.route('/')
def home():
    # """Session control"""
        # return render_template('login.html')

    if session.get('logged_in'):
        return render_template('home.html')
    else:
        return render_template('login.html')
    

@app.route('/login', methods=['POST'])
def login():
    username = request.form['id_give']
    password = request.form['password_give']  

    user = db.session.find_one({'username':username})
    if user:
        if password == user['password']:
            session['logged_in'] = True
            session['name'] = user['username']
            return jsonify({'result': 'success'})
            
    return jsonify({'result': 'fail'})

@app.route('/register/')
def register():
    return render_template('register.html')

@app.route('/register/add', methods=['POST'])
def add_user():
    new_user = {'username':request.form['id_give'], 'password':request.form['password_give']}
    db.session.insert_one(new_user)
    return jsonify({'result': 'success'})

@app.route('/home', methods=['POST'])
def post_memo():
    id_receive = request.form['id_give']  
    memo_receive = request.form['memo_give']  
    date_recieve = request.form['date_give']

    memo = {'id': id_receive, 'memo': memo_receive, 'date': date_recieve }

    db.memos.insert_one(memo)
    return jsonify({'result': 'success'})


<<<<<<< HEAD
=======

>>>>>>> e5b7663b27fd4aadb328b53a440d1d12946783bf
@app.route('/home', methods=['GET'])
def read_memos():
    result = list(db.memos.find({}, {'_id': 0}))
    return jsonify({'result': 'success', 'memos': result})
    

if __name__ == '__main__':  
    app.secret_key = "123"
    app.run('0.0.0.0', port=5000, debug=True)