import base64
import io
import uuid

import boto3
from PIL import Image

from app.config import Config


class ImageService:
    @classmethod
    def image_validation(cls, file):
        img_size = len(file) / 1024
        byte = bytearray(file)
        image_file = Image.open(io.BytesIO(byte))
        img_wid, img_hgt = image_file.size

        image_data = {"image_hight": img_hgt, "image_width": img_wid, "image_size": img_size}
        if (
            img_size <= int(Config.IMAGE_SIZE)
            and img_hgt <= int(Config.IMAGE_HIGHT)
            and img_wid <= int(Config.IMAGE_WIDTH)
        ):
            return True, image_data
        else:
            return False, image_data

    @classmethod
    def image_to_b64(cls, image):
        return base64.b64encode(image)

    @classmethod
    def b64_to_image(cls, b64):
        return base64.decodebytes(b64)

    @classmethod
    def upload_file(cls, image):
        image = cls.image_to_b64(image).decode()
        region = Config.REGION
        bucket = Config.IMAGES_S3_BUCKET

        s3 = boto3.client("s3", region_name=region)
        key = str(uuid.uuid4()) + ".txt"
        s3.put_object(Body=image, Bucket=bucket, Key=key)

        return key

    @classmethod
    def get_image(cls, key):
        region = Config.REGION
        bucket = Config.IMAGES_S3_BUCKET
        s3 = boto3.client("s3", region_name=region)
        file = s3.get_object(Bucket=bucket, Key=key)
        return file["Body"].read().decode()

    @classmethod
    def delete_image(cls, key):
        region = Config.REGION
        bucket = Config.IMAGES_S3_BUCKET

        s3 = boto3.client("s3", region_name=region)
        s3.delete_object(Bucket=bucket, Key=key)