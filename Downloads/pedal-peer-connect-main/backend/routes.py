from flask import request, jsonify
from extensions import db
from models import User
import bcrypt

def register_routes(app):

    @app.route("/register", methods=["POST"])
    def register():

        data = request.json

        full_name = data.get("full_name")
        email = data.get("email")
        phone = data.get("phone")
        password = data.get("password")

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            return jsonify({"message": "User already exists"}), 400

        hashed_password = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        new_user = User(
            full_name=full_name,
            email=email,
            phone=phone,
            password=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            "message": "User registered successfully",
            "user": new_user.to_dict()
        }), 201
    @app.route("/login", methods=["POST"])
    def login():

        data = request.json

        email = data.get("email")
        password = data.get("password")

        user = User.query.filter_by(email=email).first()

        if not user:
            return jsonify({
                "message": "User not found"
            }), 404

        password_match = bcrypt.checkpw(
            password.encode("utf-8"),
            user.password.encode("utf-8")
        )

        if not password_match:
            return jsonify({
                "message": "Invalid password"
            }), 401

        return jsonify({
            "message": "Login successful",
            "user": user.to_dict()
        }), 200