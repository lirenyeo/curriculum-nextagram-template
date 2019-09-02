import boto3, botocore
from config import Config
from flask import flash
from flask_login import current_user

s3 = boto3.client(
   "s3",
   aws_access_key_id=Config.S3_KEY,
   aws_secret_access_key=Config.S3_SECRET
)

def upload_file_to_s3(file, acl="public-read"):
    try:
        s3.upload_fileobj(
            file,
            Config.S3_BUCKET,
            f"{current_user.username}/{file.filename}",
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )
        return True

    except Exception as e:
        print("Something Happened: ", e)
        return False