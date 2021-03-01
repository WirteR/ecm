from rest_framework import serializers

from .models import Translation, User, Address
from django.db.models import Q

class UserSerializer(serializers.Serializer):
    repeat_password = serializers.CharField(required=True, style={"input_type": "password"}, write_only=True)
    password = serializers.CharField(required=True, style={"input_type": "password"}, write_only=True)
    username = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)

    def save(self, request):
        data = self.validated_data
        user = User(
            email = data.get("email"),
            username = data.get("username"),
            first_name = data.get("first_name", ""),
            last_name = data.get("last_name", ""),
            is_active = True
        )
        password = data["password"]
        repeat_password = data["password"]

        if password != repeat_password:
            raise serializers.ValidationError({"password": "passwords don't match"})

        user.set_password(password)
        try:
            user.save(request=request)    
        except:
            raise serializers.ValidationError("User already exists")
        
        return user


class TenantSerializer(UserSerializer):
    company_name = serializers.CharField(required=True)


class TranslationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Translation
        fields = [
            "lang",
            "title",
            "description"
        ]


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"


class CustomerSerializer(serializers.ModelSerializer):
    street = serializers.CharField(write_only=True)
    street_number = serializers.CharField(write_only=True)
    city = serializers.CharField(write_only=True)
    country = serializers.CharField(write_only=True)
    zip = serializers.CharField(write_only=True)
    address = AddressSerializer(many=False, read_only=True)

    class Meta:
        model = User
        fields = [
            "phone",
            "name", 
            "username",
            "account", 
            "email",
            "street", 
            "street_number",
            "city", 
            "country",
            "zip",
            "address"
        ]

    def save(self):
        address_serializer = AddressSerializer(data=self.validated_data)
        address_serializer.is_valid()
        address = address_serializer.save()
        self.clear_data()

        instance = super().save()
        
        user_qs = self.Meta.model.objects.filter(
            Q(name=self.validated_data["name"]) |
            Q(email=self.validated_data["email"]) |
            Q(phone=self.validated_data["phone"])
        )
        if user_qs.exists():
            instance = user_qs.first()
        
        instance.address = address
        instance.save()

        return instance
        
    def clear_data(self):
        model_fields = [f.name for f in self.Meta.model._meta.fields]
        for x in list(self.validated_data.keys()):
            if x not in model_fields:
                self.validated_data.pop(x)
