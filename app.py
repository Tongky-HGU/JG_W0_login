from flask import Flask, render_template, jsonify, request, session, redirect, url_for
from pymongo import MongoClient  
from bson import ObjectId
import requests

app = Flask(__name__)
client = MongoClient('localhost', 27017)
#client = MongoClient('mongodb://9jo:9jo@13.209.68.109', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
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

@app.route('/home')
def main():
    return render_template('home.html')

@app.route('/home/post', methods=['POST'])
def post_memo():
    id_receive = request.form['id_give']  
    memo_receive = request.form['memo_give']
    date_recieve = request.form['date_give']  
    anonymous_receive = request.form['anonymous']

    memo = {'id': id_receive, 'memo': memo_receive, 'date': date_recieve, 'anonymous': anonymous_receive, 'like': 0, 'dislike': 0}

    db.memos.insert_one(memo)
    return jsonify({'result': 'success'})

@app.route('/home/read', methods=['GET'])
def read_memos():
    result = list(db.memos.find({}))
    for data in result:
        data['_id'] = str(data['_id'])
    return jsonify({'result': 'success', 'memos': result})

@app.route('/home/delete', methods=['POST'])
def delete_memos():
    db_id_receive = request.form['db_id_give']
    object_id = ObjectId(db_id_receive)
    db.memos.delete_one({'_id' : object_id})
    return jsonify({'result': 'success'})

@app.route('/home/like', methods=['POST'])
def like_memos():
    db_id_receive = request.form['db_id_give']
    object_id = ObjectId(db_id_receive)
    memo = db.memos.find_one({'_id' : object_id})
    new_like = memo['like'] + 1
    db.memos.update_one({'_id' : object_id}, {'$set':{'like':new_like}})
    return jsonify({'result': 'success'})

@app.route('/home/dislike', methods=['POST'])
def dislike_memos():
    db_id_receive = request.form['db_id_give']
    object_id = ObjectId(db_id_receive)
    memo = db.memos.find_one({'_id' : object_id})
    new_dislike = memo['dislike'] + 1
    db.memos.update_one({'_id' : object_id}, {'$set':{'dislike':new_dislike}})
    return jsonify({'result': 'success'})

@app.route("/logout")
def logout():
	"""Logout Form"""
	session['logged_in'] = False
	return redirect(url_for('home'))

if __name__ == '__main__':  
    app.secret_key = "123"
    app.run('0.0.0.0', port=5000, debug=True)