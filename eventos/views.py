
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import login,logout,authenticate
from django.db import IntegrityError
from .forms import eventoForm
from .models import eventos as Evento
from django.shortcuts import get_object_or_404
from datetime import date
from django.contrib.auth.decorators import login_required

def signup(request):

    if request.user.is_authenticated:
        return redirect('eventos')

    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
    })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('eventos')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'El nombre de usuario ya existe'
                })  
                
        return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'Las contraseñas no coinciden'
                })
            
@login_required
def eventos(request):
    hoy = date.today()
    lista_evento = Evento.objects.filter(fecha_evento__gte=hoy).order_by('fecha_evento')
    return render(request, 'eventos.html', {'lista_evento': lista_evento})

@login_required
def signout(request):
    logout(request)
    return redirect('signin')

def signin(request):
    if request.user.is_authenticated:
        return redirect('eventos')

    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
    })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'Usuario o contraseña incorrectos'
            })
        else:
            login(request, user)
            return redirect('eventos')
        
@login_required
def crear_evento(request):
    
    if request.method == 'GET': 
        return render(request, 'crear_evento.html',{
            'form':eventoForm()
        })    
    else:
        form = eventoForm(request.POST)
        if form.is_valid():
            nuevo_evento = form.save(commit=False)
            nuevo_evento.creador = request.user
            nuevo_evento.save()
            return redirect('eventos')
        else:
            return render(request, 'crear_evento.html',{
                'form': form,
                'error': 'Datos no válidos, por favor corregir'
            })
@login_required            
def evento_detalle(request, evento_id):
    evento = get_object_or_404(Evento, pk=evento_id)
    
    if request.method == 'POST':
        if not request.user.is_staff:
            return HttpResponse('No tienes permisos para editar', status=403)
        
        form = eventoForm(request.POST, instance=evento)
        if form.is_valid():
            form.save()
            return redirect('eventos')
        else:
            return render(request, 'evento_detalle.html', {
                'evento': evento,
                'form': form,
                'error': 'Datos no válidos'
            })
    else:
        if request.user.is_staff:
            form = eventoForm(instance=evento)
            return render(request, 'evento_detalle.html', {
                'evento': evento,
                'form': form,
                'is_admin': True
            })
        else:
            return render(request, 'evento_detalle.html', {
                'evento': evento,
                'is_admin': False
            })
@login_required           
def eliminar_evento(request, evento_id):
    evento=get_object_or_404(Evento, pk=evento_id)
    if request.method == 'POST':
        if request.user != evento.creador and not request.user.is_staff:
            return HttpResponse('No tienes permisos para eliminar este evento', status=403)
        evento.delete()
        return redirect('eventos')
    