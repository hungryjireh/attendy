from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class AttendanceFormat(models.Model):
    datetime = models.DateTimeField(auto_now_add=True)
    #classes = models.CharField(max_length=20, choices=CLASSES)
    #campus = models.CharField(max_length=20, choices=CAMPUS_LOCATIONS)
    #student_id = models.CharField(max_length=20)
    name = models.CharField(max_length=50)
    #email = models.EmailField()
    classroom = models.ForeignKey(User, related_name='attendance', on_delete=models.CASCADE, blank=True, null=True)

class ClassroomLogin(models.Model):
    datetime = models.DateTimeField(auto_now_add=True)
    classroom_key = models.ForeignKey(User, related_name='classroom', on_delete=models.CASCADE, blank=True, null=True)
    classroom_password = models.TextField()

class NominalRoll(models.Model):
    datetime = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=50)
    saved_name = models.CharField(max_length=50)
    email = models.EmailField()
    uploaded_by = models.ForeignKey(User, related_name='nominalroll', on_delete=models.CASCADE, blank=True, null=True)