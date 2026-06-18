from mongoengine import StringField
from models.base import BaseDocument

class Message(BaseDocument):
    content = StringField(required=True)


