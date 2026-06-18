from flask import Blueprint
from models.user_model import User

user_bp = Blueprint("user", __name__, url_prefix="/user")


@user_bp.route("/u/<public_id>")
def get_user(public_id):
    user = User.objects(public_id=public_id).first()

    if not user:
        return {"message": "Not found"}, 404

    return {
        "username": user.username
    }
