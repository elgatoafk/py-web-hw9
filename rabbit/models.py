from mongoengine import Document
from mongoengine.fields import StringField, BooleanField
from bson import ObjectId

class Contacts(Document):
    fullname = StringField()
    email = StringField()
    delivered = BooleanField(default=False)

    @classmethod
    def update_delivered_by_id(cls, contact_id, delivered):
        try:
            contact = cls.objects.get(id=ObjectId(contact_id))
            contact.delivered = delivered
            contact.save()
            return "Delivered field updated successfully"
        except cls.DoesNotExist:
            return "Contact not found"