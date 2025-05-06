from rest_framework import serializers
from .models import Usuario, Alumno, Maestra, TipoDanza, Clase

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = Usuario.objects.create_user(**validated_data)
        return user

class TipoDanzaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoDanza
        fields = '__all__'

class AlumnoSerializer(serializers.ModelSerializer):
    user = UsuarioSerializer
    class Meta:
        model = Alumno
        fields = '__all__'

class MaestraSerializer(serializers.ModelSerializer):
    user = UsuarioSerializer
    class Meta:
        model = Maestra
        fields = '__all__'

class CalseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clase
        fields = '__all__'

class RegistroSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'password', 'role']



def create(self, validated_data):
    user = Usuario.objects.create_user(
        username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data['role']
    )
    return user