from flask_login import UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models.base_model import BaseModel
from playhouse.hybrid import hybrid_property
import peewee as pw
import re

class User(BaseModel, UserMixin):
    username = pw.CharField(unique=True)
    email = pw.CharField(unique=True, null=True)
    first_name = pw.CharField(unique=False, null=True)
    last_name = pw.CharField(unique=False, null=True)
    password = pw.CharField()
    description = pw.CharField(null=True)

    def validate(self):
        self.errors.append('username existed')
        self.errors.append('this always happen')


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

        if not self.password == self.password_confirm:
            self.errors.append('Confirmation password does not match')

        if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", self.email):
            self.errors.append('Invalid email address')


        # When user.save() is a create
        if self.id is None:
            if User.get_or_none(User.username == self.username):
                self.errors.append(f'Username "{self.username}" has already been taken!')

            if User.get_or_none(User.email == self.email):
                self.errors.append(f'Email "{self.email}" has already been taken!')

            self.password = generate_password_hash(self.password)
        # When user.save() is an update
        else:
            # if user change email:
            print(self.new_email, self.old_email, self.new_email != self.old_email)
            if self.new_email != self.old_email:
                if User.get_or_none(User.email == self.new_email):
                    self.errors.append(f'New email "{self.new_email}" has already been taken!')
                else:
                    self.email = self.new_email

            # if user changes password
            if self.password:
                if len(self.password) < 4:
                    self.errors.append('Password must be at least 4 characters')
                else:
                    self.password = generate_password_hash(self.password)
