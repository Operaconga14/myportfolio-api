from fastapi import APIRouter, HTTPException, status, UploadFile, File
from api.core.config.config import settings
from api.core.controllers.admin_controller import add_admin, login_admin, get_admin_details, update_admin_data, add_profile_picture, add_social_links
from api.models.schemas import AdminSchemas

router = APIRouter()


@router.get('/')
def read_admin():
    return HTTPException(status_code=status.HTTP_200_OK, detail=f"{settings.Messages.get('success').get('ok')}")


@router.get('/details')
async def get_admin():
    admin = await get_admin_details()
    return admin


@router.post('/add')
async def create_admin(admin_data: AdminSchemas.AdminCreate):
    admin = await add_admin(email=admin_data.email, username=admin_data.username, password=admin_data.password)
    return admin


@router.post('/login')
async def admin_login(admin_data: AdminSchemas.AdminLogin):
    admin = await login_admin(email=admin_data.email, password=admin_data.password)
    return admin


@router.patch('/update')
async def update_admin_info(admin_data: AdminSchemas.AdminUpdate):
    admin = await update_admin_data(**admin_data.model_dump(exclude_unset=True))
    return admin


@router.patch('/social/update')
async def update_admin_info(social_data: AdminSchemas.AdminSocials):
    admin = await add_social_links(social_data.social_url)
    return admin


@router.patch('/picture')
async def upload_picture(picture: UploadFile = File(...)):
    admin_uploaded_picture = await add_profile_picture(picture=picture)
    return admin_uploaded_picture
