from rest_framework import serializers
from django.contrib.auth.models import User
from attendance.models import AttendanceFormat, ClassroomLogin, NominalRoll

class UserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(
        style={'input_type': 'password'},
        write_only = True,
    )
    confirm_password = serializers.CharField(
        style={'input_type': 'password'},
        write_only = True,
    )
    date_joined = serializers.DateTimeField(read_only=True ,format="%Y-%m-%d %H:%M:%S")
    last_login = serializers.DateTimeField(read_only=True ,format="%Y-%m-%d %H:%M:%S")
    url = serializers.HyperlinkedIdentityField(view_name='users-detail', read_only=True)
    class Meta:
        model = User
        extra_kwargs = {
            'password': {'write_only': True},
            'url': {'view_name': 'user-detail'},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'email': {'required': True},
            'username': {'required': True},
        }
        fields = ('id', 'first_name', 'last_name', 'email', 'password', 'confirm_password', 'is_staff', 'is_superuser', 'last_login', 'date_joined', 'username', 'url')

class AttendanceFormatSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='attendance-detail', read_only=True)
    datetime = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")
    classroom = serializers.ReadOnlyField(source='classroom.username')
    class Meta:
        model = AttendanceFormat
        ordering_fields = ['-datetime']
        fields = ('datetime', 'classroom', 'name', 'url')

class ClassroomLoginSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='classroom-detail', read_only=True)
    datetime = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")
    classroom_key = serializers.ReadOnlyField(source='classroom_key.username')
    class Meta:
        model = ClassroomLogin
        ordering_fields = ['-datetime']
        lookup_field = 'classroom_key'
        fields = ('datetime', 'classroom_key', 'classroom_password', 'url')

class NominalRollSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='nominalroll-detail', read_only=True)
    datetime = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")
    uploaded_by = serializers.ReadOnlyField(source='uploaded_by.username')
    class Meta:
        model = NominalRoll
        ordering_fields = ['-datetime']
        fields = ('datetime', 'name', 'saved_name', 'email', 'uploaded_by', 'url')