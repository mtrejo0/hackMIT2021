from flask import Flask, jsonify, request
from flask_cors import CORS
from api import API
api = API()

app = Flask(__name__)
CORS(app)

@app.route('/')
def main():

    response = {
        "message": "API works!"
    }
    return jsonify(response)

@app.route('/items', methods =['GET'])
def get_items():
    try:
        response = {
            "message": "Data from some API",
            "data": api.get_items(),
        }
        return jsonify(response)
    except Exception as e:
        print(e)
        return jsonify({"error": 'Failed to get data'}), 400

@app.route('/items', methods =['POST'])
def add_item():
    try:
        item = request.json['item']
        response = {
            "message": "Added item!",
            'item': api.add_item(item)
        }
        return jsonify(response)
    except Exception as e:
        print(e)
        return jsonify({"error": 'Failed'}), 400


@app.route('/items/<id>', methods =['DELETE'])
def delete_item(id):
    try:
        api.delete_item(id)
        response = {
            "message": "Deleted item!"
        }
        return jsonify(response)
    except Exception as e:
        print(e)
        return jsonify({"error": 'Failed'}), 400

@app.route('/users', methods =['GET'])
def get_users():
    try:
        response = {
            "message": "All users",
            "users": api.get_users(),
        }
        return jsonify(response)
    except Exception as e:
        print(e)
        return jsonify({"error": 'Failed to get users'}), 400
    
@app.route('/users', methods =['POST'])
def add_user():
    try:
        username = request.json['username']
        password = request.json['password']
        response = {
            "message": "New User",
            "user": api.create_user(username, password)
        }
        return jsonify(response)
    except Exception as e:
        print(e)
        return jsonify({"error": 'Failed to add user'}), 400
    
@app.route('/users/<username>', methods =['GET'])
def get_user(username):
    try:
        response = {
            "user": api.read_user(username),
        }
        return jsonify(response)
    except Exception as e:
        print(e)
        return jsonify({"error": 'User does not exist!'}), 400

@app.route('/users/<username>', methods =['DELETE'])
def delete_user(username):
    try:
        api.delete_user(username)
        response = {
            "message": "User deleted!"
        }
        return jsonify(response)
    except Exception as e:
        print(e)
        return jsonify({"error": 'Failed to delete user'}), 400


@app.route('/login', methods =['POST'])
def login():
    try:
        username = request.json['username']
        password = request.json['password']
        response = {
            "message": "Logged in",
            "user": api.login(username, password)
        }
        return jsonify(response)
    except Exception as e:
        print(e)
        return jsonify({"error": 'Wrong login!'}), 400
    
    
if __name__ == "__main__":
    app.run(debug=True)