"""
URL configuration for subject_score_service project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from .views import subject_score_list, subject_score_detail_delete, \
    subject_score_detail, get_subject_scores

urlpatterns = [
    path('subject-scores/', subject_score_list, name='subject_score_list'),
    path('subject-scores/<int:pk>/', subject_score_detail, name='subject_score_detail'),
    path('subject-scoresd/<int:pk>/', subject_score_detail_delete, name='subject_score_detail_delete'),
    path('subject-scores/scores/', get_subject_scores, name='subject_score_by_applicant'),

]
