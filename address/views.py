from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes, permission_classes

from .serializers import AddressSerializer
from .models import Address
from user.models import User
from user.serializers import UsersSerializer

class AddressView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def put(self, request: Request):
        serializer = AddressSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        address = Address.objects.filter(**serializer.validated_data).first()
        
        if not address:
            address = Address.objects.create(**serializer.validated_data)
            
        request.user.address = address
        request.user.save()
            
        data = AddressSerializer(address).data
        
        return Response(data, status=status.HTTP_200_OK)