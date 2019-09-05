from flask_login import UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models.base_model import BaseModel
from playhouse.hybrid import hybrid_property
import peewee as pw

class User(BaseModel, UserMixin):
    username = pw.CharField(unique=True)
    email = pw.CharField(unique=False, null=True)
    first_name = pw.CharField(unique=False, null=True)
    last_name = pw.CharField(unique=False, null=True)
    password = pw.CharField()

    @hybrid_property
    def followers(self):
        from models.following import Following
        return [x.fan for x in Following.select().where(Following.idol_id == self.id)]

    @hybrid_property
    def followings(self):
        from models.following import Following
        return [x.idol for x in Following.select().where(Following.fan_id == self.id)]

    def is_following(self, user):
        return user in self.followings

    def is_followed_by(self, user):
        return user in self.followers


    @hybrid_property
    def fullname(self):
        return self.first_name + ' ' + self.last_name


    def validate_login(self, password):
        return check_password_hash(self.password, password)

    def validate(self):
        if len(self.password) < 4:
            self.errors.append('Password must be at least 4 characters')
        else:
            self.password = generate_password_hash(self.password)