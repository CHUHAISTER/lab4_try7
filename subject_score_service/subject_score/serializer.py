from .models import SubjectScore
from rest_framework import serializers


class SubjectScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectScore
        fields = '__all__'