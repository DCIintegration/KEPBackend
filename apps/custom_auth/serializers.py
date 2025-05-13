from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import CustomUser, Empleado, Departamento

# ──────────────── EMPLEADO ──────────────── #

class EmpleadoSerializer(serializers.ModelSerializer):
    departamento = serializers.PrimaryKeyRelatedField(
        queryset=Departamento.objects.all(),
        required=False,
        allow_null=True
    )

    class Meta:
        model = Empleado
        fields = [
            'id', 'nombre_completo', 'puesto',
            'fecha_contratacion', 'activo',
            'sueldo', 'departamento', 'email'
        ]

    def create(self, validated_data):
        return Empleado.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

# ──────────────── CUSTOM USER ──────────────── #

class CustomUserSerializer(serializers.ModelSerializer):
    info = EmpleadoSerializer()

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'info']


class CustomUserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    tokens = serializers.SerializerMethodField()
    info = EmpleadoSerializer()

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password', 'info', 'tokens']

    def get_tokens(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def create(self, validated_data):
        empleado_data = validated_data.pop('info')
        password = validated_data.pop('password')
        empleado = Empleado.objects.create(**empleado_data)

        user = CustomUser.objects.create_user(
            password=password,
            info=empleado,
            **validated_data
        )
        return user

# ──────────────── TOKEN JWT ──────────────── #

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        if user.info:
            token['nombre_completo'] = user.info.nombre_completo
            token['puesto'] = user.info.puesto
            token['activo'] = user.info.activo
            token['email'] = user.email
            token['departamento'] = (
                user.info.departamento.id if user.info.departamento else None
            )

        return token

# ──────────────── LOGIN ──────────────── #

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        if not data.get('email') or not data.get('password'):
            raise serializers.ValidationError("Email y contraseña son obligatorios")
        return data
