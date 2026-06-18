from datetime import timedelta

from flask import Blueprint, jsonify
from dtos.user_dto import CreateUserDto, LoginDto
from validators.validate_body import validate_body
from werkzeug.security import generate_password_hash, check_password_hash
from models.user_model import User
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, decode_token

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/register", methods=["POST"])
@validate_body(CreateUserDto)
def register(dto):
    try:
        hash_password = generate_password_hash(dto.password)

        username_taken = User.objects(username=dto.username).first()

        if username_taken:
            return {
                "status": 400,
                "message": "Username already taken",
            }, 400

        new_user = User(
            username=dto.username,
            password=hash_password
        )
        new_user.save()

        return {
            "status": 201,
            "message": "User created successfully",
            "data": {
                "username": new_user.username,
                "public_id": new_user.public_id,
                "access_token": create_access_token(
                    identity=str(new_user.id), expires_delta=timedelta(hours=24)),
                "refresh_token": create_refresh_token(
                    identity=str(new_user.id), expires_delta=timedelta(days=7)),
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

        access_token = create_access_token(
            identity=str(user.id), expires_delta=timedelta(hours=24))
        refresh_token = create_refresh_token(
            identity=str(user.id), expires_delta=timedelta(days=7))

        return jsonify({
            "status": 200,
            "message": "Logged in successfully",
            "data": {
                "access_token": access_token,
                "refresh_token": refresh_token,
            }
        })
    except Exception as e:
        return {"error": str(e)}, 400


@auth_bp.route('/refresh', methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    try:
        current_user = get_jwt_identity()
        new_token = create_access_token(
            identity=current_user, expires_delta=timedelta(hours=24))
        return jsonify({
            "status": 200,
            "message": "Token refreshed successfully",
            "data": {
                "access_token": new_token,
            }
        })
    except Exception as e:
        return {"error": str(e)}, 400


@auth_bp.route("/logout", methods=["POST"])
def logout():
    return jsonify({
        "status": 200,
        "message": "Logout successful",
    })
