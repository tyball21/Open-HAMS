import uuid

import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse

from api.deps import CurrentUser
from core.config import settings

router = APIRouter(prefix="/upload", tags=["Upload"])

# Initialize S3 client only if credentials are available
s3_client = None
if settings.AWS_ACCESS_KEY_ID and settings.AWS_SECRET_ACCESS_KEY and settings.AWS_BUCKET_NAME:
    try:
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION,
        )
    except Exception as e:
        print(f"Warning: Could not initialize S3 client: {e}")
        s3_client = None

allowed_content_types = [
    "image/jpeg",
    "image/png",
    "image/gif",
    "image/webp",
    "image/svg+xml",
    "image/jpg",
]


@router.post("/")
async def upload_file(_: CurrentUser, file: UploadFile = File(...)):
    if file.content_type not in allowed_content_types:
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    # Check if S3 is configured
    if not s3_client:
        raise HTTPException(
            status_code=503, 
            detail="File upload service not configured. Please use direct image upload in forms."
        )
    
    try:
        file_content = await file.read()
        key = str(uuid.uuid4())

        s3_client.put_object(
            Body=file_content,
            Key=key,
            Bucket=settings.AWS_BUCKET_NAME,
            ContentType=file.content_type,
        )

        file_url = f"https://{settings.AWS_BUCKET_NAME}.s3.{settings.AWS_REGION}.amazonaws.com/{key}"
        return JSONResponse({"file_url": file_url}, status_code=200)
    except (NoCredentialsError, PartialCredentialsError) as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
