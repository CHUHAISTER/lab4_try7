"""
URL configuration for subject_service project.

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

from .views import subject_list, subject_list_post, subject_detail, subject_detail_one

urlpatterns = [
    path('subjects/', subject_list, name='subject_list'),
    path('subjectsp/', subject_list_post, name='subject_list'),
    path('subjectsd/<int:pk>/', subject_detail, name='subject_detail'),
    path('subjects/<int:pk>/', subject_detail_one, name='subject_detail_one'),

]
