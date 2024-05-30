from django.shortcuts import render
import requests
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status

from .models import SubjectScore
from .serializer import SubjectScoreSerializer


# Create your views here.
@api_view(['GET', 'POST'])
def subject_score_list(request):
    if request.method == 'GET':
        subject_scores = SubjectScore.objects.all()
        serializer = SubjectScoreSerializer(subject_scores, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SubjectScoreSerializer(data=request.data)
        if serializer.is_valid():
            applicant_id = serializer.validated_data.get('applicant')
            applicant_service_url = 'http://127.0.0.1:8000/applicants'
            subject_id = serializer.validated_data.get('subject')
            subject_service_url = 'http://127.0.0.1:8004/subjects'
            try:
                applicant_response = requests.get(f'{applicant_service_url}/{applicant_id}/')
                applicant_response.raise_for_status()
                subject_response = requests.get(f'{subject_service_url}/{subject_id}/')
                subject_response.raise_for_status()
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except requests.HTTPError as e:
                error_message = f"Failed to fetch faculty information: {str(e)}"
                return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
def subject_score_detail(request, pk):
    try:
        subject_score = SubjectScore.objects.get(pk=pk)
    except SubjectScore.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SubjectScoreSerializer(subject_score)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SubjectScoreSerializer(data=request.data)
        if serializer.is_valid():
            applicant_id = serializer.validated_data.get('applicant')
            applicant_service_url = 'http://127.0.0.1:8000/applicants'
            subject_id = serializer.validated_data.get('subject')
            subject_service_url = 'http://127.0.0.1:8004/subjects'
            try:
                applicant_response = requests.get(f'{applicant_service_url}/{applicant_id}/')
                applicant_response.raise_for_status()
                subject_response = requests.get(f'{subject_service_url}/{subject_id}/')
                subject_response.raise_for_status()
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except requests.HTTPError as e:
                error_message = f"Failed to fetch faculty information: {str(e)}"
                return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        subject_score.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'DELETE'])
@permission_classes([IsAdminUser])
def subject_score_detail_delete(request, pk):
    try:
        subject_score = SubjectScore.objects.get(pk=pk)
    except SubjectScore.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SubjectScoreSerializer(subject_score)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        subject_score.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def get_subject_scores(request):
    applicant_id = request.GET.get('applicant_id')
    if not applicant_id:
        return Response({"error": "applicant is required", "r" : request.GET}, status=status.HTTP_400_BAD_REQUEST)

    try:
        subject_scores = SubjectScore.objects.filter(applicant=applicant_id)
    except SubjectScore.DoesNotExist:
        return Response({"error": "No scores found for this applicant"}, status=status.HTTP_404_NOT_FOUND)

    scores = [{"subject": score.subject, "score": score.score} for score in subject_scores]
    return Response(scores, status=status.HTTP_200_OK)