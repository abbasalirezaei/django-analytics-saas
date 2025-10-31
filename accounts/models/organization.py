from django.db import models
from django.utils.crypto import get_random_string


class Organization(models.Model):
    name = models.CharField(max_length=255)
    api_key = models.CharField(max_length=32, unique=True, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.api_key:
            self.api_key = get_random_string(32)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
