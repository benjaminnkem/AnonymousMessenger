from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user_model import User

user_bp = Blueprint("user", __name__, url_prefix="/user")


@user_bp.route("/me", methods=["GET"])
@jwt_required()
def get_me():
    user_id = get_jwt_identity()
    user = User.objects(id=user_id).first()

    if not user:
        return {"message": "Not found"}, 404

    return {
        "username": user.username,
        "public_id": user.public_id,
    }


@user_bp.route("/u/<public_id>")
def get_user(public_id):
    user = User.objects(public_id=public_id).first()

    if not user:
        return {"message": "Not found"}, 404

    return {
        "username": user.username
    }
