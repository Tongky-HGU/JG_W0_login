from flask import Flask, render_template, jsonify, request, session, redirect, url_for
from pymongo import MongoClient  
import requests

app = Flask(__name__)
client = MongoClient('localhost', 27017)
#client = MongoClient('mongodb://9jo:9jo@13.209.68.109', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.session  


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
    anonymous_receive = request.form['anonymous']

    memo = {'id': id_receive, 'memo': memo_receive, 'date': date_recieve, 'anonymous': anonymous_receive }

    db.memos.insert_one(memo)
    return jsonify({'result': 'success'})



@app.route('/home', methods=['GET'])
def read_memos():
    result = list(db.memos.find({}, {'_id': 0}))
    return jsonify({'result': 'success', 'memos': result})
    
@app.route("/logout")
def logout():
	"""Logout Form"""
	session['logged_in'] = False
	return redirect(url_for('home'))

if __name__ == '__main__':  
    app.secret_key = "123"
    app.run('0.0.0.0', port=5000, debug=True)