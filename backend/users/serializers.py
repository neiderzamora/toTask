from rest_framework import serializers
from users.models import CustomUser
from base.utils import validate_phone
from rest_framework.validators import UniqueValidator

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class CustomUserSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(validators=[validate_phone, UniqueValidator(queryset=User.objects.all(), message="Ya existe un usuario con este número de telefono.")])
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all(), message="Ya existe un usuario con este correo electrónico.")])

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("La contraseña debe exceder los 10 caracteres.")
        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError("La contraseña debe contener al menos un número.")
        if not any(char.isupper() for char in value):
            raise serializers.ValidationError("La contraseña debe contener al menos una letra mayúscula.")
        if not any(char.islower() for char in value):
            raise serializers.ValidationError("La contraseña debe contener al menos una letra minúscula.")
        if not any(char in "!@#$%^&*()" for char in value):
            raise serializers.ValidationError("La contraseña debe contener al menos un carácter especial (!@#$%^&*).")

        return value

    class Meta:
        model = CustomUser
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()