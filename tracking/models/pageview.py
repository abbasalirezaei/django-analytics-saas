from django.db import models

from tracking.models.session import Session
from tracking.models.website import Website


class PageView(models.Model):
    website = models.ForeignKey(
        Website, on_delete=models.CASCADE, related_name="pageviews"
    )
    session = models.ForeignKey(
        Session, on_delete=models.CASCADE, related_name="pageviews"
    )
    page_url = models.TextField()
    page_title = models.CharField(max_length=500, blank=True, null=True)
    referrer = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    load_time = models.FloatField(
        null=True, blank=True
    )  # Page load time in milliseconds

    user_agent = models.TextField(blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)

    class Meta:
        db_table = "page_views"
        indexes = [
            models.Index(fields=["website", "timestamp"]),
            models.Index(fields=["session"]),
            models.Index(fields=["timestamp"]),
        ]
        ordering = ["-timestamp"]

    def __str__(self):
        return f"PageView: {self.page_url}"
