from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Queja

Usuario = get_user_model()

class RegistroSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'password', 'first_name', 'primer_apellido', 'segundo_apellido', 'password', 'matricula']

    def create(self, validated_data):
        user = Usuario.objects.create_user(**validated_data)
        return user

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'first_name', 'primer_apellido', 'segundo_apellido', 'rol', 'matricula', 'fecha_registro']
        read_only_fields = ['id', 'fecha_registro', 'rol']

class CustomTokenSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        username = attrs.get('username')
        try:
            if '@' in str(username):
                user = Usuario.objects.get(email=username)
                attrs['username'] = user.username
        except Usuario.DoesNotExist:
            pass
        return super().validate(attrs)

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['rol'] = 'admin' if (user.rol == 'admin' or user.is_superuser or user.is_staff) else 'estudiante'
        return token
    
class QuejaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Queja
        fields = ['uuid', 'tipo', 'comentario', 'email', 'fecha', 'leida']
        read_only_fields = ['uuid', 'fecha', 'leida']