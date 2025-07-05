from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from src.models.user import db, User

auth_bp = Blueprint('auth', __name__)  # ✅ This must come before any routes

@auth_bp.route('/register', methods=['POST'])
def register():
    print("✅ Register route called")
    data = request.json
    print("📦 Request data:", data)

    username = data.get("username")
    email = data.get("email")
    raw_password = data.get("password")

    if not username or not email or not raw_password:
        return jsonify({"message": "Missing required fields"}), 400

    hashed_password = generate_password_hash(raw_password)

    try:
        new_user = User(username=username, email=email, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        print("✅ User created:", new_user)
        return jsonify({"message": "User registered successfully"})

    except Exception as e:
        print("❌ Registration error:", e)
        return jsonify({"message": "Internal server error"}), 500
