from imagekitio import ImageKit
import magic
from datetime import datetime
from api.core.config.config import settings


class Libraries():
    imagekit = ImageKit(
        public_key=settings.IMAGEKIT_PUBLIC_KEY,
        private_key=settings.IMAGEKIT_PRIVATE_KEY,
        url_endpoint=settings.IMAGEKIT_URL_ENDPOINT
    )
    mime = magic.Magic(mime=True)
    now = datetime.now()


libraries = Libraries()
