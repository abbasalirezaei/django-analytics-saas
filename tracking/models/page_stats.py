from django.db import models

from tracking.models.website import Website


class PageStats(models.Model):
    website = models.ForeignKey(
        Website, on_delete=models.CASCADE, related_name="page_stats"
    )
    page_url = models.TextField()
    date = models.DateField(db_index=True)

    # Page-specific metrics
    views = models.IntegerField(default=0)
    unique_visitors = models.IntegerField(default=0)
    avg_time_on_page = models.FloatField(default=0)
    exit_rate = models.FloatField(default=0)

    class Meta:
        db_table = "page_stats"
        unique_together = ["website", "page_url", "date"]
        indexes = [
            models.Index(fields=["website", "date"]),
        ]

    def __str__(self):
        return f"Page: {self.page_url} - {self.date}"
