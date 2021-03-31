from django.db.models import *


class Rifle(Model):
    title = CharField(max_length=80)
    created_at = DateTimeField('creation timestamp', auto_now_add=True)

    def __str__(self):
        return str(self.title)


class Skin(Model):
    rifles = ForeignKey(Rifle, on_delete=CASCADE)
    subject = CharField('name', max_length=80)
    text = TextField('item description', max_length=4096)
    created_at = DateTimeField('creation timestamp', auto_now_add=True)
    updated_at = DateTimeField('update timestamp', auto_now=True)

    def __str__(self):
        return str(self.subject)