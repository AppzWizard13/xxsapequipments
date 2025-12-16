# utils/management/commands/migrate_media_to_cloudinary.py

import os
from django.core.management.base import BaseCommand
from django.apps import apps
from django.conf import settings
from django.db import models

class Command(BaseCommand):
    help = "Upload local media files to Cloudinary"

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting media migration...")

        for model in apps.get_models():
            file_fields = [
                f for f in model._meta.fields
                if isinstance(f, (models.FileField, models.ImageField))
            ]

            if not file_fields:
                continue

            qs = model.objects.all()

            for obj in qs:
                updated = False

                for field in file_fields:
                    file = getattr(obj, field.name)

                    if not file:
                        continue

                    local_path = os.path.join(settings.MEDIA_ROOT, file.name)

                    if not os.path.exists(local_path):
                        continue

                    # Force re-save → triggers Cloudinary upload
                    setattr(obj, field.name, file)
                    updated = True

                if updated:
                    obj.save()
                    self.stdout.write(f"Uploaded: {obj}")

        self.stdout.write(self.style.SUCCESS("Migration completed."))
