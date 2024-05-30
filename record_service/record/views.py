from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status
import requests

from .models import Record
from .serializer import RecordSerializer


# Create your views here.
@api_view(['GET', 'POST'])
@permission_classes([IsAdminUser])
def record_list(request):
    if request.method == 'GET':
        records = Record.objects.all()
        serializer = RecordSerializer(records, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = RecordSerializer(data=request.data)
        if serializer.is_valid():
            applicant_id = serializer.validated_data.get('applicant')
            applicant_service_url = 'http://127.0.0.1:8000/applicants'
            try:
                applicant_response = requests.get(f'{applicant_service_url}/{applicant_id}/')
                applicant_response.raise_for_status()

                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except requests.HTTPError as e:
                error_message = f"Failed to fetch faculty information: {str(e)}"
                return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAdminUser])
def record_detail(request, pk):
    try:
        record = Record.objects.get(pk=pk)
    except Record.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = RecordSerializer(record)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = RecordSerializer(data=request.data)
        if serializer.is_valid():
            applicant_id = serializer.validated_data.get('applicant')
            applicant_service_url = 'http://127.0.0.1:8000/applicants'
            try:
                applicant_response = requests.get(f'{applicant_service_url}/{applicant_id}/')
                applicant_response.raise_for_status()

                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except requests.HTTPError as e:
                error_message = f"Failed to fetch faculty information: {str(e)}"
                return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        record.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


import requests


@api_view(['GET'])
@permission_classes([IsAdminUser])
def calculate_scores(request, pk):
    faculty_service_url = f'http://127.0.0.1:8001/faculties/{pk}'
    faculty_response = requests.get(faculty_service_url)

    if faculty_response.status_code != 200:
        return Response({"error": "Faculty not found."}, status=status.HTTP_404_NOT_FOUND)

    faculty = faculty_response.json()
    records = Record.objects.filter(is_approved=True)
    results = []

    for record in records:
        applicant = record.applicant

        applicant_service_url = f'http://127.0.0.1:8000/applicants/{applicant}'
        applicant_response = requests.get(applicant_service_url)
        faculty_value = applicant_response.json()["faculty"]

        if faculty_value != pk:
            continue

        response = requests.get(f'http://127.0.0.1:8003/subject-scores/scores/?applicant_id={applicant}')
        if response.status_code != 200:
            continue

        subject_scores = response.json()
        total_score = sum(score["score"] for score in subject_scores) + applicant_response.json()["certificate_score"]

        results.append({
            "applicant_id": applicant_response.json()["id"],
            "applicant_name": applicant_response.json()["name"],
            "total_score": total_score
        })


    results = sorted(results, key=lambda x: x['total_score'], reverse=True)

    enrolled_applicants = results[:faculty["intake_capacity"]]

    return Response({
        "faculty": faculty["name"],
        "enrolled_applicants": enrolled_applicants,
    }, status=status.HTTP_200_OK)
