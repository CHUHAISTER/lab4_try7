from django.db import models



class SubjectScore(models.Model):
    applicant = models.IntegerField()
    subject = models.IntegerField()
    score = models.FloatField()

    

