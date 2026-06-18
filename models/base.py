from mongoengine import DateTimeField, Document
from datetime import datetime


class BaseDocument(Document):
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    meta = {
        "abstract": True,
    }
