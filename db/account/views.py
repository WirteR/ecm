from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response

from .serializers import UserSerializer, TenantSerializer, CustomerSerializer
from db.core.models import Tenant
from .models import User
from rest_framework.authtoken.models import Token

from rest_framework.authtoken.serializers import AuthTokenSerializer

from db.db_utils import create_tenant_schema, run_command, set_tenant_for_request


class AuthorizeView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            context = {"request": request
        })
        # breakpoint()
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        user_tokens = Token.objects.filter(user=user)
        if user_tokens.exists():
            user_tokens.first().delete()
        token = Token.objects.create(user=user)

        respose = {
            "id": user.id,
            "username": user.username,
            "token": token.key,
        }

        return Response(status=200, data=respose)


class RegisterUser(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CustomerSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save(request=request)
            data = {
                "response": "User succesfully registered",
                "username": user.username,
                "email": user.email,
                "token": Token.objects.get(user=user).key
            }
        else: 
            data = serializer.errors
        
        return Response(data)


class RegisterSuperUser(APIView):
    def post(self, request, *args, **kwargs):
        serializer = TenantSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=400, data=serializer.errors)
        
        data = serializer.validated_data
        company_name = data.pop("company_name")
        data.pop("repeat_password")

        tenant, tenant_created = create_tenant_schema(company_name)
        if not tenant_created:
            return Response(status=400, data={"msg":"This company already registered"})
        
        set_tenant_for_request(tenant.id)
        try:
            user = User.objects.create(
                **data, 
                is_active=False, 
                is_superuser=True,
                tenant_id=tenant.id
            )
        except:
            tenant.delete()
            run_command(f"python {settings.BASE_DIR}/manage.py runscript update_db_conf")
            return Response(status=400, data={"msg":"This user already registered"})

        data = {
            "response": "Superuser succesfully registered",
            "username": user.username,
            "email": user.email,
            "company": tenant.company_name
        }
        return Response(data)

