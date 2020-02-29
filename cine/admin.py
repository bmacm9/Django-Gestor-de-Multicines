from django.contrib import admin
from cine.models import Pelicula, Sala, Butaca, Sesiones

# Register your models here.
admin.site.register(Pelicula)
admin.site.register(Sala)
admin.site.register(Butaca)
admin.site.register(Sesiones)
