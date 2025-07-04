from flask import Blueprint

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    return {"message": "Login route"}

@auth_bp.route('/logout', methods=['POST'])
def logout():
    return {"message": "Logout route"}
from flask import request, jsonify

@auth_bp.route('/register', methods=['POST'])
def register():
    print("Register route called")
    data = request.json
    print("Request data:", data)
    # TODO: Add your user creation logic here
    return jsonify({"message": "Registration received", "data": data})