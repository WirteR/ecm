from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny

from .serializers import CustomerSerializer, AuthCustomerSerializer, CustomerRegisterSerializer
from db.core.models import Tenant, Token
from db.helper_views import BaseAuthView
from .models import Customer


@permission_classes([AllowAny])
class AuthorizeView(BaseAuthView):
    serializer_class = AuthCustomerSerializer


@permission_classes([AllowAny])
class RegisterUser(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CustomerRegisterSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save(request=request)
            data = {
                "response": "User succesfully registered",
                "username": user.username,
                "email": user.email,
                "token": Token.objects.get(user=user.id, tenant_id=user.tenant_id).key
            }
        else: 
            data = serializer.errors
        
        return Response(data)

