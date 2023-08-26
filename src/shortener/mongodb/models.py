from mongoengine import Document, StringField, IntField, BooleanField

class URL(Document):
    key = StringField(required=True, unique=True, index=True)
    secret_key = StringField(unique=True, index=True)
    target_url = StringField(required = True)
    is_active = BooleanField(default=True)
    clicks = IntField(default = 0)
