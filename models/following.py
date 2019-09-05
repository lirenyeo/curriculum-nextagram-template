import peewee as pw
from models.base_model import BaseModel
from models.user import User

class Following(BaseModel):
   idol = pw.ForeignKeyField(User, backref='fans')
   fan = pw.ForeignKeyField(User, backref='idols')