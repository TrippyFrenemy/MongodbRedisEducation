from mongoengine import Document, StringField, ListField, ReferenceField, connect

# Підключення до MongoDB
url = "mongodb+srv://dbUser:dbUserPassword@cluster0.9fi0utw.mongodb.net/?retryWrites=true&w=majority"
connect(host=url)


class Author(Document):
    fullname = StringField(required=True, max_length=200)
    born_date = StringField(required=True, max_length=100)
    born_location = StringField(required=True)
    description = StringField()

    meta = {'collection': 'authors'}


class Quote(Document):
    tags = ListField(StringField(max_length=50))
    author = ReferenceField(Author)
    quote = StringField(required=True)

    meta = {'collection': 'quotes'}

