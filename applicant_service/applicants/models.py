from django.db import models


class Applicant(models.Model):
    name = models.CharField(max_length=100)
    faculty = models.IntegerField()
    certificate_score = models.FloatField()


    def __str__(self):
        return self.name
