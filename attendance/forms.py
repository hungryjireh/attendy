from django import forms
from .models import AttendanceFormat, NominalRoll

# class AttendanceFormatForm(forms.ModelForm):
#     class Meta:
#         model = AttendanceFormat
#         fields = ['classes', 'campus', 'student_id', 'email']

class NominalRollForm(forms.ModelForm):
    class Meta:
        model = NominalRoll
        fields = ['name', 'email']