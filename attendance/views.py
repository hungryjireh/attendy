from attendance.models import AttendanceFormat, ClassroomLogin, NominalRoll
from attendance.forms import NominalRollForm
from attendance.serializers import AttendanceFormatSerializer, UserSerializer, ClassroomLoginSerializer, NominalRollSerializer
from django import forms
from django.http import HttpResponseBadRequest, HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.core.exceptions import PermissionDenied
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.messages import constants as messages
from django.shortcuts import redirect, render
from rest_framework import viewsets, filters, status, generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
import requests, random, string
from datetime import datetime
import netifaces
import logging
import csv

SF_DEFAULT_GATEWAY = "10.0.0.1" #TBC

# Create your views here.
def attendance_page(request):
    date = str(datetime.date(datetime.now()))
    if request.method == 'GET':
        objectlist = NominalRoll.objects.all().order_by('name')
        if not request.user.is_superuser and request.user.is_authenticated:
            classroom_info = ClassroomLogin.objects.get(classroom_key=request.user)
            return render(request, 'navigationguide.html', {'objectlist': objectlist, 'date': date, 'classroom_key': classroom_info.classroom_key, 'classroom_password': classroom_info.classroom_password})
        else:
            return render(request, 'navigationguide.html', {'objectlist': objectlist, 'date': date})
    else:
        if "new-class" in request.POST:
            class_username = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(6))
            class_password = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(6))
            print(class_username)
            print(class_password)
            User.objects.create_user(class_username, '', class_password)
            user = authenticate(username=class_username, password=class_password)
            user_object = User.objects.get(username=class_username)
            classroom_info = ClassroomLogin.objects.create(classroom_key=user_object, classroom_password=class_password)
            classroom_info.save()
            if user is not None:
                login(request, user)
                return redirect('/')
        else:
            name_field = request.POST.get('name')
            gateways = netifaces.gateways()
            default_gateway = gateways['default'][netifaces.AF_INET][0]
            if default_gateway == SF_DEFAULT_GATEWAY:
                attendance_list = AttendanceFormat.objects.create(classroom=request.user, name=name_field)
                attendance_list.save()   
                return render(request, 'navigationguide.html', {'date': date, 'status_message': "✓ Attendance submitted successfully!"})
            else:
                return render(request, 'navigationguide.html', {'date': date, 'status_message': "✗ You're not connected to the campus wifi and can't mark attendance!"})

@staff_member_required
def upload_csv(request):
    data = {}
    if "GET" == request.method:
        return render(request, "csvupload.html", data)
    # if not GET, then proceed
    try:
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):
            messages.error(request,'File is not CSV type')
            return HttpResponseRedirect('/')
        #if file is too large, return
        if csv_file.multiple_chunks():
            messages.error(request,"Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000),))
            return HttpResponseRedirect('/')
        
        file_data = csv_file.read().decode("utf-8")		
        
        lines = file_data.split("\n")
		#loop over the lines and save them in db. If error , store as string and then display
        for line in lines:						
            fields = line.split(",")
            data_dict = {}
            data_dict["name"] = fields[0]
            data_dict["email"] = fields[1]
            try:
                form = NominalRollForm(data_dict)
                if form.is_valid():
                    form = NominalRoll.objects.update_or_create(uploaded_by=request.user, name=form.cleaned_data['name'], saved_name=form.cleaned_data['name'].lower().replace(" ", "_"), email=form.cleaned_data['email'])
                    form.save()
                else:
                    logging.getLogger("error_logger").error(form.errors.as_json())
            except Exception as e:
                logging.getLogger("error_logger").error(repr(e))
                pass
    except Exception as e:
        logging.getLogger("error_logger").error("Unable to upload file. "+repr(e))
        messages.error(request,"Unable to upload file. "+repr(e))
    return HttpResponseRedirect('/')

@staff_member_required
def download_csv_page(request):
    if request.method == 'GET':
        query = User.objects.all()
        query_list = [item for item in query if item.username != "jireh"]
        print(query_list)
        return render(request, 'csvdownload.html', {'query_list': query_list})
    else:
        name_field = request.POST.get('username')
        classroom = User.objects.get(username=name_field)
        return download_csv(classroom)

@staff_member_required
def download_csv(classroom):
    response = HttpResponse(content_type='text/csv')
    filename = str(classroom) + ".csv"
    response['Content-Disposition'] = 'attachment; filename="{0}"'.format(filename)
    writer = csv.writer(
        response,
        delimiter=',',
        quotechar='"',
        quoting=csv.QUOTE_ALL
    )
    query = AttendanceFormat.objects.filter(classroom=classroom).values('name')
    query_list = [item['name'] for item in list(query)]
    for f in NominalRoll.objects.filter(saved_name__in=query_list):
        writer.writerow([f.datetime, f.name, f.email])
    return response

class UserViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('username', 'email')

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        user = self.request.user
        if (self.request.user.is_superuser):
            return User.objects.all()
        else:
            return User.objects.filter(is_staff=False, is_superuser=False, username=user.username)

class UserDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        profile = self.get_object(pk)
        serializer = UserSerializer(profile, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        profile = self.get_object(pk)
        serializer = UserSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        profile = self.get_object(pk)
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class AttendanceFormatView(viewsets.ModelViewSet):
    queryset = AttendanceFormat.objects.all()
    serializer_class = AttendanceFormatSerializer
    permission_classes = (IsAdminUser,)
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('datetime', 'classroom')

    def perform_create(self, serializer):
        serializer.save(classroom=self.request.user)

class AttendanceFormatDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return AttendanceFormat.objects.get(pk=pk)
        except AttendanceFormat.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        profile = self.get_object(pk)
        serializer = AttendanceFormatSerializer(profile, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        profile = self.get_object(pk)
        serializer = AttendanceFormatSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        profile = self.get_object(pk)
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ClassroomLoginView(viewsets.ModelViewSet):
    queryset = ClassroomLogin.objects.all()
    serializer_class = ClassroomLoginSerializer
    permission_classes = (IsAdminUser,)
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('datetime', 'classroom_key', 'classroom_password')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ClassroomLoginDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return ClassroomLogin.objects.get(pk=pk)
        except ClassroomLogin.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        profile = self.get_object(pk)
        serializer = ClassroomLoginSerializer(profile, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        profile = self.get_object(pk)
        serializer = ClassroomLoginSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        profile = self.get_object(pk)
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class NominalRollView(viewsets.ModelViewSet):
    queryset = NominalRoll.objects.all()
    serializer_class = NominalRollSerializer
    permission_classes = (IsAdminUser,)
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('datetime')

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)

class NominalRollDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return NominalRoll.objects.get(pk=pk)
        except NominalRoll.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        profile = self.get_object(pk)
        serializer = NominalRollSerializer(profile, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        profile = self.get_object(pk)
        serializer = NominalRollSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        profile = self.get_object(pk)
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)