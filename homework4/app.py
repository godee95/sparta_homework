from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

from pymongo import MongoClient

# client = MongoClient('localhost', 27017)
client = MongoClient('mongodb://test:test@localhost', 27017)
db = client.dbhomework


## HTML 화면 보여주기
@app.route('/')
def homework():
    return render_template('index.html')


# 주문하기(POST) API
@app.route('/order', methods=['POST'])
def save_order():
    name_receive = request.form['name_give']
    count_receive = request.form['count_give']
    address_receive = request.form['address_give']
    phone_receive = request.form['phone_give']

    # 입력 데이터 DB에 저장하기 위해 딕셔너리 생성
    doc = {
        'name': name_receive,
        'count': count_receive,
        'address': address_receive,
        'phone': phone_receive
    }
    # DB에 저장
    db.shopping.insert_one(doc)

    return jsonify({'msg': '주문 저장 완료!'})


# 주문 목록보기(Read) API
@app.route('/order', methods=['GET'])
def view_orders():
    shopping = list(db.shopping.find({}, {'_id': False}))
    return jsonify({'all_shopping':shopping})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)