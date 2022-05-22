from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import authenticate

from .serializers import UsersSerializer, LoginSerializer
from .models import User
from .permissions import UserAuthenticated


class UsersView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [UserAuthenticated]
    
    def get(self, _: Request):
        users = User.objects.all()
        serializer = UsersSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request: Request):
        serializer = UsersSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        found_user = User.objects.filter(email=serializer.validated_data['email']).exists()
        
        if found_user:
            return Response({"message": "User already exists"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        user = User.objects.create(**serializer.validated_data)
        
        user.set_password(serializer.validated_data['password'])
        user.save()
        
        serializer = UsersSerializer(user)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
@api_view(['POST'])
def login_view(request: Request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    found_user = authenticate(
        request,
        username=serializer.validated_data['email'],
        password=serializer.validated_data['password']
    )
    
    if found_user is None:
        return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    
    token = Token.objects.get_or_create(user=found_user)[0]
    
    return Response({"token": token.key}, status=status.HTTP_200_OK) 