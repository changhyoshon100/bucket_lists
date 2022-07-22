from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient

client = MongoClient("mongodb+srv://test:sparta@cluster0.pfrwvbn.mongodb.net/?retryWrites=true&w=majority")
db = client.dbsparta
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')
# //num,bucket,done
@app.route('/bucket', methods=['POST'])
def bucket_post():
    bucket_receive = request.form['bucket_give']

    num = len(list(db.buckets.find({}, {'_id': False})))
    done = 0
    doc = {
        'num': num,
        'bucket': bucket_receive,
        'done': done
    }
    db.buckets.insert_one(doc)
    return jsonify({'msg': 'post success!'})

@app.route('/bucket', methods=['GET'])
def bucket_get():
    buckets = list(db.buckets.find({}, {'_id':False}))
    return jsonify({'buckets': buckets})

@app.route('/done', methods=['POST'])
def bucket_done():
    num = request.form['num_give']
    print('num=',num)

    db.buckets.update_one({'num': int(num)}, {'$set': {'done': 1}})

    buckets = list(db.buckets.find({}, {'_id': False}))
    print(buckets[1]['done'])
    return jsonify({'result': 'done!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)