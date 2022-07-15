from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbsparta

## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('index.html')

## API 역할을 하는 부분
@app.route('/review', methods=['POST'])
def write_review():
    title_receive = request.form['title_give']
    author_receive = request.form['author_give']
    review_receive = request.form['review_give']

    # 입력 데이터 DB에 저장하기 위해 딕셔너리 생성
    doc = {
        'title':title_receive,
        'author':author_receive,
        'review':review_receive
    }
    # DB에 저장
    db.bookreview.insert_one(doc)

    # return jsonify({'msg': '이 요청은 POST!'})
    return jsonify({'msg': '저장 완료!'})


@app.route('/review', methods=['GET'])
def read_reviews():
    # sample_receive = request.args.get('sample_give')
    # print(sample_receive)

    #클라이언트에서 값을 받을 필요 없고 DB데이터 가져오면 됨.
    reviews = list(db.bookreview.find({}, {'_id': False}))

    # return jsonify({'msg': '이 요청은 GET!'})
    return jsonify({'all_reviews': reviews})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)