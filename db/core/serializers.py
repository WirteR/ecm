from rest_framework import serializers
from .models import Superuser, SuperuserGroup, SuperuserPermission
from db.helper_serializers import GroupSerializer
from rest_framework.exceptions import ValidationError
from django.db.models import Q


class AuthAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Superuser
        fields = [
            "username",
            "password"
        ]
        extra_kwargs = {
            "username": {"validators": []}
        }
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        if username and password:
            users = self.Meta.model.objects.filter(
                Q(username=username) |
                Q(phone=username) |
                Q(email=username)
            )
            if users.exists():
                user = users.first()
                valid = user.check_password(password)
                if not valid:
                    raise serializers.ValidationError("Password is not correct")
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class RegisterSerializer(serializers.Serializer):
    repeat_password = serializers.CharField(required=True, style={"input_type": "password"}, write_only=True)
    password = serializers.CharField(required=True, style={"input_type": "password"}, write_only=True)
    username = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    phone = serializers.CharField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)

    def validate(self, attrs):
        password = attrs["password"]
        repeat_password = attrs["password"]
        if password != repeat_password:
            raise serializers.ValidationError({"password": "passwords don't match"})
        return attrs


class TenantRegisterSerializer(RegisterSerializer):
    company_name = serializers.CharField(max_length=128)


class SuperuserPermissionSerializer(serializers.ModelSerializer):
    group = serializers.PrimaryKeyRelatedField(queryset=SuperuserGroup.objects.all(), required=False)

    class Meta:
        model = SuperuserPermission
        fields = "__all__"


class SuperuserGroupSerializer(GroupSerializer):
    permissions = SuperuserPermissionSerializer(many=True, read_only=True)
    group_permissions = serializers.DictField(child=serializers.CharField(), write_only=True)
    class Meta:
        permission_serializer = SuperuserPermissionSerializer
        model = SuperuserGroup
        fields = "__all__"

        