from models.base_model import BaseModel
from models.post import Post
import peewee as pw


class Endorsement(BaseModel):
    amount = pw.DecimalField(decimal_places=2)
    post = pw.ForeignKeyField(Post, backref="endorsements")


