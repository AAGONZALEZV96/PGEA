from django.db import models
from django.contrib.auth.models import AbstractBaseUser
# Create your models here.


class Usuario(AbstractBaseUser):
    ROLES =(
        ('ADMIN', 'Administrador'),
        ('MAEST', 'Maestra'),
        ('ALUM', 'Alumno'),
    )
    role = models.CharField(max_length=5, choices=ROLES)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    

#danza y nivel

class TipoDanza(models.Model):
    name = models.CharField(max_length=50)
    level = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} - {self.level}"
    

#alumno

class Alumno(models.Model):
    user = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='perfil_alumno')
    rut = models.CharField(max_length=12 , unique=True)
    edad = models.PositiveIntegerField()
    fecha_insc =models.DateField()
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    tipo_danza = models.ForeignKey(TipoDanza, on_delete=models.SET_NULL, null=True)
    asistencia = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.rut})"
    

#Maestra

class Maestra(models.Model):
    user = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='perfil_maestra' )
    rut = models.CharField(max_length=12 , unique=True)
    edad = models.PositiveIntegerField()
    fecha_insc =models.DateField()
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    tipo_danza = models.ForeignKey(TipoDanza, on_delete=models.SET_NULL, null=True)
    asistencia = models.BooleanField(default=False)
    alumnos = models.ManyToManyField(Alumno, related_name='maestras')

    def __str__(self):
        return self.user.__get_full_name()
    
    def alumnos_list(self):
        return self.alumnos.count()
    
#clases

class Clase(models.Model):
    name = models.CharField(max_length=100)
    tipo_danza = models.ForeignKey(TipoDanza, on_delete=models.CASCADE)
    maestra =models.ForeignKey(Maestra, on_delete=models.SET_NULL, null=True)
    alumnos = models.ManyToManyField(Alumno)
    fecha = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return f"{self.name} ({self.tipo_danza}) - ({self.fecha})"
 

