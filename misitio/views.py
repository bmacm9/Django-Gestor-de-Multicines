from django.http import HttpResponse, Http404

from django.shortcuts import render
from cine.models import Pelicula, Sesiones, Butaca
from cine.forms import FormularioReserva
from misitio.settings import EMAIL_HOST_USER
from django.core.mail import send_mail

def main(request):
    ''' Nos devuelve la pagina principal'''
    return render(request, 'main.html')

def cartelera(request):
    ''' Obtiene las peliculas que tenemos y las muestra '''
    context = {}
    diccionarioPeliculas = []
    peliculas = Pelicula.objects.filter()
    for pelicula in peliculas:
        diccionarioPeliculas.append(pelicula)

    context['peliculas'] = diccionarioPeliculas
    print(context)


    return render(request, 'cartelera.html', context)

def about(request):
    ''' Nos devuelve la pagina de Sobre Mi '''
    return render(request, 'about.html')


def sesiones(request, pelicula):
    ''' Para la pelicula seleccionada por el usuario pasada como parametro, obtenemos las sesiones que hay y las mostramos '''
    contexto = {}
    diccionarioSesiones = []
    seleccionada = Pelicula.objects.get(titulo=pelicula)
    sesiones = Sesiones.objects.filter(pelicula__titulo = pelicula)
    for sesion in sesiones:
        diccionarioSesiones.append(sesion)

    contexto['pelicula'] = seleccionada
    contexto['sesiones'] = diccionarioSesiones
    return render(request, 'sesiones.html', contexto);


def pelicula(request, pelicula, sesion):
    ''' dada la sesion de una pelicula pasada como parametro obtenemos los datos de la pelicula y la sesion y devolveremos una pagina con ellos '''

    #Obteniendo datos de los modelos
    sesionSelec = Sesiones.objects.get(id = sesion)
    seleccionada = Pelicula.objects.get(titulo = pelicula)

    #montando un array de butacas seleccionados por el usuario en el formulario por POST
    butacas = Butaca.objects.filter(sesion=sesionSelec)
    arrayButacas = []
    for butacaOcupada in butacas.values():
        arrayButacas.append(butacaOcupada['numero'])

    #Los datos que le pasaremos a la pagina
    contexto = {
        "sesionSelec": sesionSelec,
        "seleccionada": seleccionada,
        "butacas": arrayButacas,
        "sesion": sesion
    }

    #renderizando la pagina
    return render(request, 'pelicula.html', contexto)


def reservar(request, pelicula, sesion):
    ''' El usuario ha rellenado un formulario con los asientos que quiere, los reservamos en la base de datos'''

    butacas = []
    if request.method == 'POST':
        for e in request.POST:
            if 'csrf' not in e:
                butacas.append(e)

    f = FormularioReserva()
    seleccionada = Pelicula.objects.get(titulo = pelicula)

    contexto = {
        "form": f,
        "sesion": sesion,
        "seleccionada": seleccionada,
        "butacas": butacas
    }
    return render(request, 'reservar.html', contexto)


def comprar(request, pelicula, sesion):
    sesionSelec = Sesiones.objects.get(id=sesion)
    if request.method == 'POST':
        for butaca in request.POST.getlist("butacas"):
            butacaNueva = Butaca(numero=butaca, sesion=sesionSelec)
            butacaNueva.save()
        email = request.POST["email"]
        asunto = "Sobre la compra de sus entradas en Granada Cine"
        fecha = sesionSelec.fecha.strftime("%d/%m/%Y")
        hora = sesionSelec.hora.strftime("%H:%M:%S")
        mensaje = "Gracias por la compra de sus entradas para la pelicula " + pelicula + " para la sesion de " + fecha + " a las " + hora + ". Disfrute de la pelicula!"
    send_mail(asunto, mensaje, EMAIL_HOST_USER, [email], fail_silently=False)
    return render(request, "gracias.html")