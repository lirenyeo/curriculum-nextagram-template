from models.base_model import BaseModel
from models.user import User
from config import Config
from playhouse.hybrid import hybrid_property
import peewee as pw

class Post(BaseModel):
    image_path = pw.CharField(null=False)
    user = pw.ForeignKeyField(User, backref='posts', null=False)

    @hybrid_property
    def image_full_url(self):
        return f"https://{Config.S3_BUCKET}.s3-ap-southeast-1.amazonaws.com/{self.image_path}"