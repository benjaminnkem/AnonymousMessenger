from mongoengine import StringField
from models.base import BaseDocument
from nanoid import generate

class User(BaseDocument):
    username = StringField(required=True, unique=True)
    password = StringField(required=True)
    public_id = StringField(default=lambda: generate(size=10), unique=True)

    meta = {
        "collection": "users",
        "strict": False,
    }
