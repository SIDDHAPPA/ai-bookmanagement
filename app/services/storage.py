import boto3
from app.config import settings
from app.services.text_extractor import extract_text_from_pdf

session = boto3.session.Session()

s3 = session.client(
    "s3",
    region_name=settings.DO_SPACES_REGION,
    endpoint_url=settings.DO_SPACES_ENDPOINT,
    aws_access_key_id=settings.DO_SPACES_KEY,
    aws_secret_access_key=settings.DO_SPACES_SECRET,
)

BUCKET = settings.DO_SPACES_BUCKET


def upload_file(file_obj, key: str, content_type: str):
    s3.upload_fileobj(
        file_obj,
        BUCKET,
        key,
        ExtraArgs={
            "ACL": "private",
            "ContentType": content_type
        }
    )
    return key


def get_file_content(key: str) -> str:
    obj = s3.get_object(Bucket=BUCKET, Key=key)
    data = obj["Body"].read()

    if key.lower().endswith(".pdf"):
        return extract_text_from_pdf(data)

    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return ""