import peewee as pw
from peewee import fn
from models.base_model import BaseModel
from models.user import User
from playhouse.hybrid import hybrid_property


class Following(BaseModel):
    idol = pw.ForeignKeyField(User, backref='fans')
    fan = pw.ForeignKeyField(User, backref='idols')

    @hybrid_property
    def uid(self):
        return str(self.idol_id) + '-' + str(self.fan_id)

    @uid.expression
    def uid(cls):
        return fn.CONCAT(cls.idol_id, '-', cls.fan_id)