from django.db import models

from accounts.models import Organization


class Website(models.Model):
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="websites"
    )
    name = models.CharField(max_length=255)
    domain = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "websites"
        indexes = [
            models.Index(fields=["domain"]),
            models.Index(fields=["organization", "created_at"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.domain})"
