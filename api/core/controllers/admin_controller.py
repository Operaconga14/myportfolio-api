import io
from typing import Optional
from api.models.model import Admin
from fastapi import HTTPException, UploadFile, status, Response, Request
from passlib.context import CryptContext
from api.core.config.config import settings
from api.core.config.libraries import libraries
from datetime import datetime, timedelta, timezone
from api.models.model import Admin
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions


pwd_cont = CryptContext(schemes=['bcrypt'], deprecated="auto")


# Hash the admin password
def hash_password(password: str):
    return pwd_cont.hash(password)


# Verify the store password and the admin given password
def verify_password(password: str, stored_hashed_password: str):
    return pwd_cont.verify(password, stored_hashed_password)


# Register admin
async def add_admin(email: str, username: str, password: str):
    try:
        admin_count = await Admin.all().count()

        if admin_count >= 1:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"{settings.Messages.get('error').get('only_one')}")

        existing_admin = await Admin.get_or_none(email=email)

        if existing_admin:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=settings.Messages.get('error').get('email_exist'))

        hashed_password = hash_password(password=password)
        new_admin = await Admin(email=email, username=username, password=hashed_password)
        new_admin.created_at = libraries.now
        await new_admin.save()

        return new_admin
    except HTTPException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"{e}")


# Admin Login
async def login_admin(email: str, password: str):
    try:
        admin = await Admin.get_or_none(email=email)

        if admin is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"{settings.Messages.get('error').get('no_admin')}")

        if not verify_password(password=password, stored_hashed_password=admin.password):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"{settings.Messages.get('error').get('password')}")

        return {"message": f"Admin {settings.Messages.get('success').get('login')}"}

    except HTTPException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"{e}")


async def get_admin_details():
    try:
        admin = await Admin.first()

        if admin is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"{settings.Messages.get('error').get('no_admin')}")

        return {
            "full_name": admin.full_name,
            "first_name": admin.first_name,
            "last_name": admin.last_name,
            "username": admin.username,
            "email": admin.email,
            "picture": admin.picture,
            "socials": admin.social_url,
            "contact": admin.contact,
            "location": admin.location,
            "created_at": admin.created_at,
            "updated_at": admin.updated_at
        }
    except HTTPException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"{e}")


# Update Admin
async def update_admin_data(**kwargs):
    try:
        admin = await Admin.first()

        if admin is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"{settings.Messages.get('error').get('no_admin')}")

        update_data = {
            key: value for key,
            value in kwargs.items() if value is not None
        }

        if not update_data:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"{settings.Messages.get('error').get('empty_field')}")

        for fields, value in update_data.items():
            setattr(admin, fields, value)

        admin.updated_at = libraries.now
        await admin.save()

        return {"message": f"Account {settings.Messages.get('success').get('update')}"}
    except HTTPException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}")


async def add_social_links(social_link: str):
    try:
        admin = await Admin.first()

        if admin is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"{settings.Messages.get('error').get('no_admin')}")

        existing_social_link = admin.social_url or []

        if not isinstance(existing_social_link, list):
            existing_social_link = []

        existing_social_link.append(social_link)
        admin.social_url = existing_social_link
        admin.updated_at = libraries.now
        await admin.save()
        return {"message": f"Social Link {settings.Messages.get('success').get('update')}"}
    except HTTPException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}")


async def add_profile_picture(picture: UploadFile):
    try:

        if picture is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"{settings.Messages.get('error').get('empty_field')}")

        admin = await Admin.first()

        if admin is None or not admin:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"{settings.Messages.get('error').get('no_admin')}")

        file_data = await picture.read()
        file_mime_type = libraries.mime.from_buffer(file_data)

        valid_extensions = {
            "image/png": ".png",
            "image/jpeg": ".jpg",
            "image/gif": ".gif"
        }

        if file_mime_type not in valid_extensions:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"{settings.Messages.get('error').get('file_type_support')}")

        file_extension = valid_extensions[file_mime_type]
        file_name = f"{admin.first_name}{admin.last_name}{file_extension}"
        file_stream = io.BytesIO(file_data)
        file_stream.seek(0)

        upload = libraries.imagekit.upload_file(
            file=("file", file_stream, file_mime_type),
            file_name=file_name,
            options=UploadFileRequestOptions(
                use_unique_file_name=False,
                folder="/my_api/admin_picture/",
                overwrite_file=False
            )
        )

        upload_url = upload.url if upload else None
        if not upload_url:
            raise HTTPException(status_code=500, detail="File upload failed.")

        admin.picture = upload_url
        admin.updated_at = libraries.now
        await admin.save()

        return {"message": f"Image {settings.Messages.get('success').get('upload')}", "profile_Image": admin.picture}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}")
