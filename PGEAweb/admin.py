from django.contrib import admin
from .models import Usuario, Alumno, Maestra, TipoDanza, Clase


# Register your models here.
admin.site.register(Usuario)
admin.site.register(Alumno)
admin.site.register(Maestra)
admin.site.register(TipoDanza)
admin.site.register(Clase)