from django.conf import settings
from django.db import models

# Create your models here.
class ConsentRecord(models.Model):
    """
    A model to store records of user consent for the gf_cookies app.
    Each record includes information about the user, session, IP, timestamp, and consent type.

    Fields:
        user (ForeignKey): A reference to the user who gave consent. Nullable.
        session_id (CharField): A string field to store the session ID. Nullable.
        ip (CharField): A string field to store the IP address of the user. Nullable.
        timestamp (DateTimeField): Automatically records the timestamp when the consent record is created.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.CharField(max_length=250, null=True, blank=True)
    ip = models.CharField(max_length=250, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    consent_type = models.CharField(max_length=10)