from django.db import models

from tracking.models.session import Session
from tracking.models.website import Website


class Event(models.Model):
    website = models.ForeignKey(
        Website, on_delete=models.CASCADE, related_name="events"
    )
    session = models.ForeignKey(
        Session, on_delete=models.CASCADE, related_name="events"
    )
    event_name = models.CharField(max_length=100, db_index=True)
    event_data = models.JSONField(blank=True, null=True)  # Flexible event payload
    page_url = models.TextField(blank=True, null=True)  # URL where event occurred
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "events"
        indexes = [
            models.Index(fields=["website", "event_name", "timestamp"]),
            models.Index(fields=["session"]),
            models.Index(fields=["timestamp"]),
        ]
        ordering = ["-timestamp"]

    def __str__(self):
        return f"Event: {self.event_name} - {self.website.domain}"
