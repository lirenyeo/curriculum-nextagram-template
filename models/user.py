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

    @hybrid_property
    def fullname(self):
        return self.first_name + ' ' + self.last_name

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

            if self.password:
                if not re.match(r"^(?=.*[0-9])(?=.*[a-zA-Z])([a-zA-Z0-9]+){4,}$", self.password):
                    self.errors.append("Password must be at least 4 characters long, and contain at least one digit and one letter.")

                self.password = generate_password_hash(self.password)
            else:
                self.errors.append('Password must not be blank')

        # When user.save() is an update
        else:
            # if user change email:
            if self.email != self.old_email:
                if User.get_or_none(User.email == self.email):
                    self.errors.append(f'New email "{self.email}" has already been taken!')

            # if user changes password
            if self.password:
                if not re.match(r"^(?=.*[0-9])(?=.*[a-zA-Z])([a-zA-Z0-9]+){4,}$", self.password):
                    self.errors.append("Password must be at least 4 characters long, and contain at least one digit and one letter.")
                else:
                    self.password = generate_password_hash(self.password)
            # if user leaves password field blank during profile edit
            else:
                # get back the user's old password (should find a better approach for this)
                actual_pass = User.get_by_id(self.id).password
                self.password = actual_pass
