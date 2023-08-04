from mongoengine import *
from mongoengine.queryset import QuerySet
import configparser
import os

# host = config['PROD']['DB_URI']
dbName = os.environ["DB_NAME"]
dbUsername = os.environ["DB_USERNAME"]
dbPassword = os.environ["DB_PASS"]
dbPort = os.environ["DB_PORT"]
dbHost = os.environ["DB_HOST"]

#host = f"mongodb://{dbUsername}:{dbPassword}@{hostname}:{dbPort}/{dbName}?retryWrites=true&w=majority"
host = f"mongodb://{dbUsername}:{dbPassword}@{dbHost}:{dbPort}"
print(host)
connection = connect(host=host)   

class User(Document):
    name = StringField(required=True)
    email = EmailField(required=True, unique=True)
    pwd = StringField(required=True)
    def __init__(self, *args, **values):
        super().__init__(*args, **values)
        User.save(self=self)

    def to_json(self):
        return {
            "_id": str(self.pk),
            "name": self.name,
            "email": self.email,
}
