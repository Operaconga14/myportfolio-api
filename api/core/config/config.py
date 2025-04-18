import os
from typing import List
from dotenv import load_dotenv
import ssl


load_dotenv()


class Settings():
    ssl_context = ssl.create_default_context()

    # Project and Security
    PROJECT_NAME: str = "My Portfolio API"
    API_VI_STR: str = "/api/v1"

    # DB
    DB_CONFIG = {
        'connections': {
            'default': {
                'engine': 'tortoise.backends.mysql',
                'credentials': {
                    'host': os.getenv("DB_HOST"),
                    'port': int(os.getenv("DB_PORT")),
                    'user': os.getenv("DB_USER"),
                    'password': os.getenv("DB_PASSWORD"),
                    'database': os.getenv("DB_NAME"),
                    'ssl':  ssl_context

                }
            }
        },
        'apps': {
            'models': {
                'models': ["api.models.model"],
                'default_connection': 'default',
            }
        }
    }
    # Cors
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost",
        "http://localhost:8000",
        "http://localhost:3000",
        "https://amirejoseph.netlify.app"
    ]

    IMAGEKIT_PRIVATE_KEY: str = os.getenv("IMAGEKIT_PRIVATE_KEY")
    IMAGEKIT_PUBLIC_KEY: str = os.getenv("IMAGEKIT_PUBLIC_KEY")
    IMAGEKIT_URL_ENDPOINT: str = os.getenv("IMAGEKIT_URL_ENDPOINT")

    # Messages
    Messages = {
        "error": {
            "registration": "Failed to register",
            "login": "Failed to login try again",
            "password": "Incorrect Password",
            "email_exist": "Email already exist",
            "server_error": "Server error try again",
            "no_admin": "Admin not found",
            "invalid_token": "Invalid token",
            "empty_field": "No field provided",
            "logged_out": "You've already logged out",
            "file_type_support": "Unsupported file type",
            "not_logged_in": "You need to log in",
            "not_found": "Does not exist",
            "only_one": "Only one Admin is allowed"
        },
        "success": {
            "ok": "Site is okay",
            "login": "Login successful",
            "registration": "Registration successful",
            "welcome": "Welcome to My Portfolio Api",
            "logout": "You've logged out successfully",
            "update": "Updated successfully",
            "deleted": "Deleted successfully",
            "upload": "Uploaded successfully",
        }
    }

    class Config:
        case_sensitive = True


settings = Settings()
