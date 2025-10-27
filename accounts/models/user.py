from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    organization = models.ForeignKey(
        'accounts.Organization', on_delete=models.CASCADE, related_name='users', null=True, blank=True
    )

    role = models.CharField(
        max_length=20,
        choices=[
            ('admin', 'Administrator'),
            ('user', 'User'),
            ('viewer', 'Viewer'),
        ],
        default='user'
    )

    class Meta:
        db_table = 'users'

    def __str__(self):
        org_name = self.organization.name if self.organization else 'NoOrg'
        return f"{self.username} ({org_name})"
