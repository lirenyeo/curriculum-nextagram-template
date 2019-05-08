from models.base_model import BaseModel
import peewee as pw
from flask_login import UserMixin

class User(BaseModel, UserMixin):
    name = pw.CharField(unique=False)
