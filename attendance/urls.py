"""attendy_test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf.urls import url
from rest_framework import routers
from django.conf.urls.static import static
from django.views.generic.base import TemplateView # new
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from attendance import views

router = routers.DefaultRouter()
router.register(r'attendance', views.AttendanceFormatView, basename='attendance')
router.register(r'users', views.UserViewSet, basename='users')
router.register(r'classroom', views.ClassroomLoginView, basename='classroom')
router.register(r'nominalroll', views.NominalRollView, basename='nominalroll')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin-home/', include(router.urls)),
    url(r'^$', views.attendance_page, name='home'),
    path('upload/', views.upload_csv, name='upload'),
    path('download-attendance/', views.download_csv_page, name='download'),
    path('admin-home/attendance/<int:pk>/', views.AttendanceFormatDetail.as_view(), name='attendance-detail'),
    path('admin-home/users/<int:pk>/', views.UserDetail.as_view(), name='users-detail'),
    path('admin-home/classroom/<int:pk>/', views.ClassroomLoginDetail.as_view(), name='classroom-detail'),
    path('admin-home/nominalroll/<int:pk>/', views.NominalRollDetail.as_view(), name='nominalroll-detail'),
]
