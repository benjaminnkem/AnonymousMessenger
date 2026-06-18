from flask import request
from flask.sansio.blueprints import Blueprint

message_bp = Blueprint('message', __name__, url_prefix='/message')

@message_bp.route('/', methods=['POST', 'GET'])
def message():

    if request.method == "POST":
        return ""

    return ""
