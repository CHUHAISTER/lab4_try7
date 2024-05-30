import requests
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status

from .models import Applicant
from .serializers import ApplicantSerializer


# Create your views here.
@api_view(['GET', 'POST'])
def applicant_list(request):
    if request.method == 'GET':
        applicants = Applicant.objects.all()
        serializer = ApplicantSerializer(applicants, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ApplicantSerializer(data=request.data)
        if serializer.is_valid():
            faculty_id = serializer.validated_data.get('faculty')
            faculty_service_url = 'http://127.0.0.1:8001/faculties'
            try:
                faculty_response = requests.get(f'{faculty_service_url}/{faculty_id}/')
                faculty_response.raise_for_status()

                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except requests.HTTPError as e:
                error_message = f"Failed to fetch faculty information: {str(e)}"
                return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT'])
def applicant_detail(request, pk):
    try:
        applicant = Applicant.objects.get(pk=pk)
    except Applicant.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ApplicantSerializer(applicant)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ApplicantSerializer(data=request.data)
        if serializer.is_valid():
            faculty_id = serializer.validated_data.get('faculty')
            faculty_service_url = 'http://127.0.0.1:8001/faculties'
            faculty_response = requests.get(f'{faculty_service_url}/{faculty_id}/')
            faculty_response.raise_for_status()

            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE'])
@permission_classes([IsAdminUser])
def applicant_detail_delete(request, pk):
    try:
        applicant = Applicant.objects.get(pk=pk)
    except Applicant.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ApplicantSerializer(applicant)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        applicant.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
