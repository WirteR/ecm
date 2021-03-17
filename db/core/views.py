from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.authtoken.views import ObtainAuthToken 
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from .serializers import AuthAdminSerializer, TenantRegisterSerializer, SuperuserGroupSerializer
from db.helper_views import BaseAuthView
from db.db_utils import create_tenant_schema, run_command, set_tenant_for_request
from .models import Superuser, SuperuserGroup
from django.conf import settings


@permission_classes([AllowAny])
class AuthorizeAdmin(BaseAuthView):
    serializer_class = AuthAdminSerializer


@permission_classes([AllowAny])
class RegisterAdmin(APIView):
    def post(self, request, *args, **kwargs):
        serializer = TenantRegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=400, data=serializer.errors)
        
        data = serializer.validated_data
        company_name = data.pop("company_name")
        data.pop("repeat_password")
        password = data.pop("password")

        tenant, tenant_created = create_tenant_schema(company_name)
        if not tenant_created:
            return Response(status=400, data={"msg":"This company already registered"})
        
        set_tenant_for_request(tenant.id)
        try:
            user = Superuser.objects.create(
                **data, 
                is_active=False, 
                is_superuser=True,
                is_staff=True,
                tenant=tenant
            )
            user.set_password(password)
            user.save()
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


class SuperuserGroupViewset(ModelViewSet):
    model_class = SuperuserGroup
    queryset = model_class.objects.all()
    serializer_class = SuperuserGroupSerializer

