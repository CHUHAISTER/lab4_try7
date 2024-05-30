from django.db import models
from django.contrib.auth.models import User


class Record(models.Model):
    applicant = models.IntegerField()
    reviewed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)
    reviewed_at = models.DateTimeField(auto_now_add=True)
