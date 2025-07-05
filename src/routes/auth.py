from flask import request, jsonify
from src.models.user import db, User
from flask_bcrypt import Bcrypt
from sqlalchemy.exc import IntegrityError

bcrypt = Bcrypt()

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        if not username or not email or not password:
            return jsonify({"message": "Missing required fields"}), 400

        # Check if user exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return jsonify({"message": "Username already taken"}), 400

        # Hash the password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Create user (IMPORTANT: match the model field name exactly)
        new_user = User(username=username, email=email, password_hash=hashed_password)

        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "User registered successfully"}), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({"message": "Email already registered"}), 400

    except Exception as e:
        print("❌ Registration error:", e)
        return jsonify({"message": "Internal server error"}), 500
