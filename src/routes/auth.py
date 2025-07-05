from flask import request, jsonify
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError
from src.models.user import db, User  # Make sure this import matches your structure

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"message": "Invalid JSON payload"}), 400

        username = data.get("username", "").strip()
        email = data.get("email", "").strip().lower()
        raw_password = data.get("password", "")

        # ✅ Basic validation
        if not username or not email or not raw_password:
            return jsonify({"message": "All fields are required"}), 400

        if len(raw_password) < 6:
            return jsonify({"message": "Password must be at least 6 characters"}), 400

        # ✅ Check if user already exists
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            return jsonify({"message": "Username or email already registered"}), 409

        # ✅ Hash password and create user
        hashed_password = generate_password_hash(raw_password)
        new_user = User(username=username, email=email, password_hash=hashed_password)

        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "User registered successfully"}), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({"message": "Database integrity error — possibly a duplicate"}), 400

    except Exception as e:
        print(f"❌ Registration error: {e}")
        return jsonify({"message": "Something went wrong on the server"}), 500
