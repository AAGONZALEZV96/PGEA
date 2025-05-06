from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import  AlumnoViewSet, ClaseViewSet, LoginView, MaestraViewSet, RegistroView, TipoDanzaViewSet, UsuarioViewSet, AlumnosPorMaestraView, login_view
from .api import router
router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)
router.register(r'alumnos', AlumnoViewSet)
router.register(r'maestras', MaestraViewSet)
router.register(r'tipo-danza', TipoDanzaViewSet)
router.register(r'clases', ClaseViewSet)


urlpatterns = [
    path('api/', include(router.urls)),
    path('registro/', RegistroView.as_view(), name='registro'),
    path('login/', login_view, name='login'),
    path('mis-alumnos/', AlumnosPorMaestraView.as_view(), name='mis_alumnos'),

    
]