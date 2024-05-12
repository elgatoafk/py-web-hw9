from mongoengine import Document
from mongoengine.fields import ReferenceField,  ListField, StringField


class Authors(Document):
    name = StringField(required=True)
    born_date = StringField(required=True)
    born_location = StringField(required=True)
    description = StringField(required=True)


class Quotes(Document):
    tags = ListField(StringField(max_length=50))
    author = ReferenceField(Authors, required=True)
    quote = StringField(required=True)