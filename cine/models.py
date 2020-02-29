from django.db import models

# Create your models here.


class Pelicula(models.Model):
    id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=30)
    autor = models.CharField(max_length=30)
    portada = models.ImageField(upload_to='static/css/')
    descripcion = models.TextField()
    edadMinima = models.CharField(max_length=2)

    def __str__(self):
        return self.titulo


class Sala(models.Model):
    numero = models.IntegerField()

    def __str__(self):
        return 'Sala: {}'.format(self.numero)


class Sesiones(models.Model):
    fecha = models.DateField()
    hora = models.TimeField()
    pelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE)
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE)

    def __str__(self):
        return 'Sesión de {} de {} a las {}'.format(self.pelicula, self.fecha, self.hora)


class Butaca(models.Model):
    numero = models.IntegerField()
    sesion = models.ForeignKey(Sesiones, on_delete=models.DO_NOTHING)

    def __str__(self):
        return 'Butaca {}, {}'.format(self.numero, self.sesion)
