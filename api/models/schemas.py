from pydantic import BaseModel
from typing import Optional, List


class AdminSchemas():
    class AdminCreate(BaseModel):
        email: str
        username: str
        password: str

    class AdminLogin(BaseModel):
        email: str
        password: str

    class AdminUpdate(BaseModel):
        first_name: Optional[str] = None
        last_name: Optional[str] = None
        contact: Optional[str] = None
        location: Optional[str] = None

    class AdminResponse(BaseModel):
        id: int
        first_name: Optional[str] = None
        last_name: Optional[str] = None
        email: str
        social_url: Optional[List[str]] = []
        username: Optional[str] = None
        contact: Optional[str] = None
        location: Optional[str] = None
        created_at: Optional[str] = None
        updated_at: Optional[str] = None
        picture: Optional[str] = None
        message: str

        class Config:
            orm_mode = True

    class AdminSocials(BaseModel):
        social_url: Optional[List[str]] = None

    class SocialLink(BaseModel):
        platform: str
        url: str
        icon: Optional[str] = None

    class AdminPicture(BaseModel):
        picture: Optional[str] = None


class PersonalProjectSchemas():
    class PersonalProjectCreate(BaseModel):
        name: str
        image: Optional[str] = None
        description: str
        urls: Optional[List[str]] = []
        tech_stack: Optional[List[str]] = []
        status: str  # Should match the ProjectStatus enum
        is_completed: bool = False

    class PersonalProjectUpdate(BaseModel):
        name: Optional[str] = None
        image: Optional[str] = None
        description: Optional[str] = None
        urls: Optional[List[str]] = None
        tech_stack: Optional[List[str]] = None
        status: Optional[str] = None  # Should match the ProjectStatus enum
        is_completed: Optional[bool] = None


class PersonalProjectResponse(BaseModel):
    id: int
    name: str
    image: Optional[str] = None
    description: str
    urls: Optional[List[str]] = []
    tech_stack: Optional[List[str]] = []
    status: str
    is_completed: bool
    created_at: Optional[str] = None
    update_at: Optional[str] = None
    posted_by: Optional[int] = None

    class Config:
        orm_mode = True


class FeaturedProjectSchemas():
    class FeaturedProjectCreate(BaseModel):
        name: str
        image: Optional[str] = None
        description: str
        urls: Optional[List[str]] = []
        tech_stack: Optional[List[str]] = []
        status: str  # Should match the ProjectStatus enum
        is_completed: bool = False

    class FeaturedProjectUpdate(BaseModel):
        name: Optional[str] = None
        image: Optional[str] = None
        description: Optional[str] = None
        urls: Optional[List[str]] = None
        tech_stack: Optional[List[str]] = None
        status: Optional[str] = None  # Should match the ProjectStatus enum
        is_completed: Optional[bool] = None

    class FeaturedProjectResponse(BaseModel):
        id: int
        name: str
        image: Optional[str] = None
        description: str
        urls: Optional[List[str]] = []
        tech_stack: Optional[List[str]] = []
        status: str  # Should match the ProjectStatus enum
        is_completed: bool
        created_at: Optional[str] = None
        update_at: Optional[str] = None
        posted_by: Optional[int] = None

        class Config:
            orm_mode = True


class TechStackSchemas():
    class TechStackCreate(BaseModel):
        name: str
        image: Optional[str] = None

    class TechStackUpdate(BaseModel):
        name: Optional[str] = None
        image: Optional[str] = None

    class TechStackResponse(BaseModel):
        id: int
        name: str
        image: Optional[str] = None
        posted_by: Optional[int] = None

        class Config:
            orm_mode = True


class ServiceSchemas():
    class ServiceCreate(BaseModel):
        name: str
        description: Optional[str] = None
        image: Optional[str] = None

    class ServiceUpdate(BaseModel):
        name: Optional[str] = None
        description: Optional[str] = None
        image: Optional[str] = None

    class ServiceResponse(BaseModel):
        id: int
        name: str
        description: Optional[str] = None
        image: Optional[str] = None
        posted_by: Optional[int] = None

        class Config:
            orm_mode = True
