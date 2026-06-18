from flask import Blueprint

from dtos.message_dto import MessageDto
from validators.validate_body import validate_body
from models.message_model import Message
from models.user_model import User
from flask_jwt_extended import jwt_required, get_jwt_identity

message_bp = Blueprint('message', __name__, url_prefix='/message')


@message_bp.route('/all', methods=['GET'])
@jwt_required()
def get_messages():
    try:
        user_id = get_jwt_identity()
        user = User.objects(id=user_id).only("public_id").first()

        public_id = user.public_id
        messages = Message.objects(public_id=public_id).order_by('-created_at')

        return {
            "status": 200,
            "message": "Message list created successfully",
            "data": [message.to_dict() for message in messages]
        }
    except Exception as e:
        return {
            "status": 500,
            "message": str(e)
        }, 500


@message_bp.route('/create', methods=['POST'])
@validate_body(MessageDto)
def message(dto: MessageDto):
    try:
        user = User.objects(public_id=dto.public_id).first()
        if not user:
            return {
                "status": 404,
                "message": "User with this public id does not exist"
            }, 404

        new_message = Message(content=dto.content, public_id=dto.public_id, role=dto.role)
        new_message.save()

        return {
            "status": 201,
            "message": "Message created successfully"
        }, 201
    except Exception as e:
        return {
            "status": 400,
            "message": str(e)
        }
