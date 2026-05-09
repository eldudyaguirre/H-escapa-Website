from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from datetime import datetime
import json
from django.http import JsonResponse
from django.db import transaction
from datetime import date, timedelta
import string
import random
import subprocess


def home(request):
    return render(request, 'index.html')

def homein(request):
    return render(request, 'frm-menpri.html')

def do_signin(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('homein')
            else:
                messages.error(request, 'Usuario o contraseña inválidos.')
        else:
            messages.error(request, 'Usuario o contraseña inválidos.')        
    
    form = AuthenticationForm()
    return render(request, 'sign-in.html', {'signin_form': form})

def do_logout(request):
    logout(request)
    return redirect('home')
            
def about(request):
    return render(request, 'about.html')

def contactanos(request):
    return render(request, 'contact.html')

def agendamiento(request):
    return render(request, 'book-appointment.html')

def ayudasos(request):
    return render(request, 'ayuda-sos.html')

def coupletherapy(request):
    return render(request, 'couple-therapy.html')

def depansitherapy(request):
    return render(request, 'depansi-therapy.html')

def grupaltherapy(request):
    return render(request, 'grupal-therapy.html')

def guerrerovaliente(request):
    return render(request, 'guerrero-valiente.html')

def individualtherapy(request):
    return render(request, 'individual-therapy.html')

def kidstherapy(request):
    return render(request, 'kids-therapy.html')

def judgeservices(request):
    return render(request, 'judgeservices.html')

def kchetazomental(request):
    return render(request, 'kchetazo-mental.html')

def meditation(request):
    return render(request, 'meditation.html')

def services(request):
    return render(request, 'services.html')

def signinuser(request):
    return render(request, 'signin-user.html')

def signin(request):
    return render(request, 'signin-admin.html')

def teamhp(request):
    return render(request, 'team-hp.html')

def bloggeneral(request):
    return render(request, 'blog.html')

def blogdetalle(request):
    return render(request, 'blog-single.html')

def homeincalendario(request):
    # Obtener offset de semana (?week=1 o ?week=-1)
    week_offset = int(request.GET.get("week", 0))

    hoy = date.today()

    # Encontrar lunes de la semana actual
    inicio_semana = hoy - timedelta(days=hoy.weekday())
    inicio_semana += timedelta(weeks=week_offset)

    fin_semana = inicio_semana + timedelta(days=6)

    dias_semana = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
    meses = ["Ene", "Feb", "Mar", "Abr", "May", "Jun",
             "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]

    dias = []

    for i in range(7):
        dia = inicio_semana + timedelta(days=i)

        dias.append({
            "nombre": dias_semana[dia.weekday()],
            "numero": dia.day,
            "mes": meses[dia.month - 1],
            "fecha": dia
        })

    horas = [f"{h:02d}:00" for h in range(8, 23)]

    rango = f"{inicio_semana.day} {meses[inicio_semana.month-1]} – {fin_semana.day} {meses[fin_semana.month-1]} {fin_semana.year}"

    context = {
        "dias": dias,
        "horas": horas,
        "rango": rango,
        "week_offset": week_offset
    }

    return render(request, "frm-calendario.html", context)

def homeinnuevopaciente(request):
    return render(request, 'frm-nuevopaciente.html')