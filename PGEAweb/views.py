from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from rest_framework import viewsets, permissions, generics
from .models import Usuario, Alumno, Maestra, TipoDanza, Clase
from .serializers import RegistroSerializer, UsuarioSerializer,AlumnoSerializer, MaestraSerializer, TipoDanzaSerializer, CalseSerializer
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
# Create your views here.

def inicio(request):
    return render(request,'inicio.html')


class EsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'ADMIN'

class EsMaestra(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'PROF'

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [EsAdmin]

    

class AlumnoViewSet(viewsets.ModelViewSet):
    queryset = Alumno.objects.all()
    serializer_class = AlumnoSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == 'PROF':
            maestra = user.perfil_maestra
            return maestra.alumnos.all()
        return super().get_queryset()

class MaestraViewSet(viewsets.ModelViewSet):
    queryset = Maestra.objects.all()
    serializer_class = MaestraSerializer
    permission_classes = [EsMaestra]

class TipoDanzaViewSet(viewsets.ModelViewSet):
    queryset = TipoDanza.objects.all()
    serializer_class = TipoDanzaSerializer
    permission_classes = [EsAdmin, EsMaestra]#ojo aqui

class ClaseViewSet(viewsets.ModelViewSet):
    queryset = Clase.objects.all()
    serializer_class = CalseSerializer
    permission_classes = [EsAdmin]

class RegistroView(generics.CreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = RegistroSerializer
    permission_classes = [permissions.AllowAny]

    def registro_view(request):
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect('inicio')
        else:
            form = UserCreationForm()
        return render(request,'registro.html', {'form': form})


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        from django.contrib.auth import authenticate
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({'error': 'Invalid Credentials'}, status=400)
    
class AlumnosPorMaestraView(generics.ListAPIView):
    serializer_class = AlumnoSerializer

    def get_queryset(self):
        maestra = Maestra.objects.get(user=self.request.user)
        return Alumno.objects.filter(clase__maestra=maestra)
    

def login_view(request):
    return render(request,'login.html')


def registro_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('inicio')
    else:
        form = UserCreationForm()
    return render(request,'registro.html', {'form': form})



@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request, format=None):
    return Response({
        'usuarios': reverse('usuario-list', request=request, format=format),
        'registro': reverse('registro', request=request, format=format),
        'login': reverse('login', request=request, format=format),
        'mis-alumnos': reverse('mis_alumnos', request=request, format=format),
    })