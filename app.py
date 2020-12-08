from flask import Flask, render_template, session
from pymongo import MongoClient  

app = Flask(__name__)

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.

db = client.week1  # 'dbsparta'라는 이름의 db를 만들거나 사용합니다.

# class User():
#     id = db.Column(db.Interger,primar)
    

@app.route('/')
def home():
    # """Session control"""
    if session.get('logged_in'):
        return render_template('home.html')
    else:
        return render_template('login.html')
    

@app.route('/login', methods=['POST'])
def login():
    id_receive = request.form['id_give']  
    password_receive = request.form['password_give']  

    user = {'id': id_receive, 'password': password_receive }

    db.users.insert_one(user)

    return jsonify({'result': 'success'})


if __name__ == '__main__':  
   app.run('0.0.0.0', port=5000, debug=True)