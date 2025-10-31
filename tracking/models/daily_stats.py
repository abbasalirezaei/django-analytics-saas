from django.db import models

from tracking.models.website import Website


class DailyWebsiteStats(models.Model):
    website = models.ForeignKey(
        Website, on_delete=models.CASCADE, related_name="daily_stats"
    )
    date = models.DateField(db_index=True)

    # Metrics
    pageviews = models.IntegerField(default=0)
    unique_visitors = models.IntegerField(default=0)
    sessions = models.IntegerField(default=0)
    events = models.IntegerField(default=0)
    avg_session_duration = models.FloatField(default=0)

    # Bounce rate, conversion rate, etc.
    bounce_rate = models.FloatField(default=0)

    class Meta:
        db_table = "daily_website_stats"
        unique_together = ["website", "date"]
        indexes = [
            models.Index(fields=["website", "date"]),
        ]

    def __str__(self):
        return f"Stats for {self.website.domain} on {self.date}"
