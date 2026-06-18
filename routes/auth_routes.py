from datetime import timedelta

from flask import Blueprint, jsonify
from dtos.user_dto import CreateUserDto, LoginDto
from validators.validate_body import validate_body
from werkzeug.security import generate_password_hash, check_password_hash
from models.user_model import User
from flask_jwt_extended import create_access_token

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/register", methods=["POST"])
@validate_body(CreateUserDto)
def register(dto):
    try:
        hash_password = generate_password_hash(dto.password)

        username_taken = User.objects(username=dto.username).first()
        email_taken = User.objects(email=dto.email).first()

        if username_taken:
            return {
                "status": 400,
                "message": "Username already taken",
            }, 400

        if email_taken:
            return {
                "status": 400,
                "message": "Email already taken",
            }, 400

        new_user = User(
            username=dto.username,
            email=dto.email,
            password=hash_password
        )
        new_user.save()

        return {
            "status": 201,
            "message": "User created successfully",
            "data": {
                "username": new_user.username,
                "access_token": create_access_token(identity=str(new_user.id), expires_delta=timedelta(hours=24)),
            }
        }, 201

    except Exception as e:
        return {"error": str(e)}, 400


@auth_bp.route('/login', methods=["POST"])
@validate_body(LoginDto)
def login(dto):
    try:
        user = User.objects(username=dto.username).first()

        if not user:
            return {
                "status": 401,
                "message": "User does not exist",
            }, 401

        password_valid = check_password_hash(user.password, dto.password)
        if not password_valid:
            return {
                "status": 401,
                "message": "Incorrect password",
            }

        token = create_access_token(identity=str(user.id))

        return jsonify({
            "status": 200,
            "message": "Logged in successfully",
            "data": {
                "access_token": token,
            }
        })
    except Exception as e:
        return {"error": str(e)}, 400


@auth_bp.route("/logout", methods=["POST"])
def logout():
    return "Logout"
