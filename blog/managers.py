from django.db import models
from django.utils import timezone

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            status='PB',
            publish__lte=timezone.now()
        )

