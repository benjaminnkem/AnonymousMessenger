from mongoengine import StringField
from models.base import BaseDocument


class Message(BaseDocument):
    content = StringField(required=True)
    role = StringField(required=True)
    public_id = StringField(required=True)

    def to_dict(self):
        return {
            "id": str(self.id),
            "public_id": self.public_id,
            "role": self.role,
            "content": self.content,
            "created_at": self.created_at.isoformat()
            if self.created_at else None
        }
