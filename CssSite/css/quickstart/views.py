from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from quickstart.serializers import UserSerializer, GroupSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.files import File
import random
import string


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


@api_view(['GET', 'POST'])
def submitFile(request):
    if request.method == 'GET':
        return  Response(status=status.HTTP_201_CREATED)

    elif request.method == 'POST':
        print('submit new file')
        dataStoreFile = handle_uploaded_file(request.FILES['dataFile'])
        merkleStoreFile = handle_uploaded_file(request.FILES['merkleFile'])
        #
        return  Response(status=status.HTTP_200_OK)

def index(req):
    return render(req, 'index.html')

def handle_uploaded_file(f):
    print(f)
    fileName = generateFileName()
    with open('storage/'+fileName+'.txt   ', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return fileName+'.txt'

def generateFileName():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=20))

@api_view(['POST'])
def challenge(request):
    print('start challenge with request')
    print(request)
    #
    return  Response(status=status.HTTP_200_OK)