import logging
from django.conf import settings
from django.db.models import Max
logger = logging.getLogger(__name__)
from PIL import Image
import io
import os
from django.core.files.uploadedfile import InMemoryUploadedFile

def compress_image(file, max_size_kb=300, quality_step=5, min_quality=20):
    img = Image.open(file)
    img_format = 'JPEG'

    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")

    quality = 95
    while quality >= min_quality:
        buffer = io.BytesIO()
        img.save(buffer, format=img_format, quality=quality)
        size_kb = buffer.tell() / 1024
        if size_kb <= max_size_kb:
            break
        quality -= quality_step

    buffer.seek(0)
    new_image = InMemoryUploadedFile(
        buffer,
        'ImageField',
        file.name,
        'image/jpeg',
        buffer.tell(),
        None
    )
    return new_image
