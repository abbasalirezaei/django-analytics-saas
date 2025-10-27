from django.db import models
from tracking.models.website import Website


class Session(models.Model):
    """
    Represents a user's browsing session on a specific website.

    A session tracks the start and end time of a user's visit, along with metadata such as
    browser type, device type, IP address, and country. Each session is uniquely identified
    by a session_id and is linked to a Website instance.

    This model is useful for analytics, tracking user behavior, and calculating metrics like
    session duration, bounce rate, and active users.
    """

    website = models.ForeignKey(
        Website,
        on_delete=models.CASCADE,
        related_name='sessions',
        help_text="The website to which this session belongs."
    )
    session_id = models.CharField(
        max_length=100,
        db_index=True,
        help_text="Unique identifier for the session."
    )
    started_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the session started."
    )
    ended_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Timestamp when the session ended (if available)."
    )
    user_agent = models.TextField(
        blank=True,
        null=True,
        help_text="User agent string from the browser."
    )
    ip_address = models.GenericIPAddressField(
        blank=True,
        null=True,
        help_text="IP address of the user during the session."
    )
    country = models.CharField(
        max_length=2,
        blank=True,
        null=True,
        help_text="ISO country code of the user."
    )
    browser = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Browser name used during the session."
    )
    device_type = models.CharField(
        max_length=20,
        choices=[
            ('desktop', 'Desktop'),
            ('mobile', 'Mobile'),
            ('tablet', 'Tablet'),
        ],
        blank=True,
        null=True,
        help_text="Type of device used during the session."
    )

    class Meta:
        db_table = 'sessions'
        indexes = [
            models.Index(fields=['session_id']),
            models.Index(fields=['website', 'started_at']),
        ]
        unique_together = ['website', 'session_id']

    def __str__(self):
        return f"Session {self.session_id} - {self.website.domain}"