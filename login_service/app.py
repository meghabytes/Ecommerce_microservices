from flask import Flask, request, jsonify, render_template, redirect
from pymongo import MongoClient
from flask_cors import CORS  # Import Flask-CORS

app = Flask(__name__)
CORS(app)
client = MongoClient("mongodb://mongodb-service:27017/")  

db = client["login_db"]
collection = db["users"]

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    # Check if user exists in the database
    user_document = collection.find_one({'username': username})

    if user_document:
        # Convert ObjectId to string
        user_document['_id'] = str(user_document['_id'])
        # Extract userID and return a JSON response
        userID = user_document['userID']
        # Return JSON indicating success with redirection link
        return jsonify({'message': 'Login successful', 'redirect_url': f'http://192.168.49.2:30363/products?userID={userID}'})
    else:
        # If user doesn't exist, return a JSON response with an error message
        return jsonify({'message': 'User does not exist, please sign up'}), 400  # Status 400 for bad request


@app.route('/signup', methods=['POST'])
def signup():
    username = request.form.get('username')  # No need to check request.method; POST is enforced by the decorator
    password = request.form.get('password')

    # Check if the username already exists
    if collection.find_one({'username': username}):
        return jsonify({'message': 'Username already exists!'}), 400

    # Generate a new userID based on the maximum existing userID
    max_user = collection.find_one(sort=[("userID", -1)])
    userID = max_user["userID"] + 1 if max_user else 1

    # Insert the new user into the collection
    new_user = {'userID': userID, 'username': username, 'password': password}
    collection.insert_one(new_user)

    return jsonify({'message': 'Signup successful', 'userID': userID})  # Ensure JSON response

if __name__ == '__main__':
    app.run(port=5000, debug=True)
