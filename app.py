from flask import Flask
from flask_pymongo import PyMongo
from bson.json_util import dumps 
from bson.objectid import ObjectId
from flask import jsonify, request

app= Flask(__name__)
app.secret_key= "secretkey"
app.config['MONGO_URI']= "mongodb+srv://minhnguyen001:minhlun2210@sandbox.rlgbu.mongodb.net/test"
mongo = PyMongo(app)
db= "MindX"
col= "test"
@app.route('/add', methods =['POST'])
def add_user():
    _json = request.json
    _achievement = _json['Achievements']
    _class = _json['Mã lớp']
    _name = _json['Tên học sinh']
    
    if _name and _class and _achievement and request.method =="POST":
        id =   mongo.db.col.insert_one({'Achievements': _achievement, 'Mã lớp':_class, 'Tên học sinh': _name })
        resp= jsonify("Student added successfully")
        resp.status_code =200

        return resp
    else:
        return not_found()

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status':404,
        'message': 'Not Found' + request.url
    }
    resp = jsonify(message)
    resp.status_code =404
    return resp

@app.route('/users', methods = ['GET'])
def users():
    users= mongo.db.col.find()
    resp = dumps(users)
    return resp

@app.route('/users/<id>', methods = ['GET'])
def user(id):
    user = mongo.db.col.find_one({'_id':ObjectId(id)})
    resp = dumps(user)
    return resp

@app.route('/delete/<id>',methods=['DELETE'])
def delete_user(id):
    mongo.db.col.delete_one({'id':ObjectId(id)})
    resp = jsonify("User deleted successfully")
    resp.status_code = 200
    return resp

@app.route('/update/<id>',methods=['PUT'])
def update_user(id):
    _id = id
    _json = request.json
    _achievement = _json['Achievements']
    _class = _json['Mã lớp']
    _name = _json['Tên học sinh']
 
    if _achievement and _class and _id and _name and request.method == "PUT":
 
        mongo.db.col.update_one({'_id':ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},{'$set':{'Achievements': _achievement, 'Mã lớp':_class, 'Tên học sinh': _name }})
 
        resp = jsonify("User updated successfully")
 
        resp.status_code = 200
 
        return resp
 
    else:
 
        return not_found()
if __name__ == "__main__":
    app.run(debug=True)
