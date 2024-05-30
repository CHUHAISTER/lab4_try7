"""
URL configuration for faculty_service project.

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

from .views import faculty_list, faculty_detail, faculty_list_post, faculty_detail_one

urlpatterns = [
    path('faculties/', faculty_list, name='faculty_list'),
    path('facultiesp/', faculty_list_post, name='faculty_list_post'),
    path('facultiesd/<int:pk>/', faculty_detail, name='faculty_detail'),
    path('faculties/<int:pk>/', faculty_detail_one, name='faculty_detail_one'),

]
