from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import get_object_or_404, redirect, render
from datetime import date, timedelta

from .models import Post


def home(request):
    return render(request, "index.html")


def do_signin(request):
    if request.user.is_authenticated:
        return redirect("homein")
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect(request.GET.get("next") or "homein")
        messages.error(request, "Usuario o contraseña inválidos.")
    else:
        form = AuthenticationForm(request)
    return render(request, "signin-admin.html", {"signin_form": form})


def do_logout(request):
    logout(request)
    return redirect("home")


def signin(request):
    return do_signin(request)


def about(request): return render(request, "about.html")
def contactanos(request): return render(request, "contact.html")
def agendamiento(request): return render(request, "book-appointment.html")
def ayudasos(request): return render(request, "ayuda-sos.html")
def coupletherapy(request): return render(request, "couple-therapy.html")
def depansitherapy(request): return render(request, "depansi-therapy.html")
def grupaltherapy(request): return render(request, "grupal-therapy.html")
def guerrerovaliente(request): return render(request, "guerrero-valiente.html")
def individualtherapy(request): return render(request, "individual-therapy.html")
def kidstherapy(request): return render(request, "kids-therapy.html")
def judgeservices(request): return render(request, "judgeservices.html")
def kchetazomental(request): return render(request, "kchetazo-mental.html")
def meditation(request): return render(request, "meditation.html")
def services(request): return render(request, "services.html")
def signinuser(request): return render(request, "signin-user.html")
def teamhp(request): return render(request, "team-hp.html")


def bloggeneral(request):
    posts = (
        Post.objects.filter(estado="PUBLICADO")
        .select_related("categoria", "autor")
        .prefetch_related("etiquetas")
    )
    return render(request, "blog-dinamico.html", {"posts": posts})


def blogdetalle(request, slug):
    post = get_object_or_404(
        Post.objects.select_related("categoria", "autor").prefetch_related("etiquetas"),
        slug=slug,
        estado="PUBLICADO",
    )
    return render(request, "blog-detalle-dinamico.html", {"post": post})


@login_required(login_url="signin")
def homein(request):
    return render(request, "frm-menpri.html")


@login_required(login_url="signin")
def homeincalendario(request):
    week_offset = int(request.GET.get("week", 0))
    hoy = date.today()
    inicio_semana = hoy - timedelta(days=hoy.weekday()) + timedelta(weeks=week_offset)
    fin_semana = inicio_semana + timedelta(days=6)
    dias_semana = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
    meses = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
    dias = []
    for i in range(7):
        dia = inicio_semana + timedelta(days=i)
        dias.append({"nombre": dias_semana[dia.weekday()], "numero": dia.day, "mes": meses[dia.month - 1], "fecha": dia})
    horas = [f"{h:02d}:00" for h in range(8, 23)]
    rango = f"{inicio_semana.day} {meses[inicio_semana.month-1]} – {fin_semana.day} {meses[fin_semana.month-1]} {fin_semana.year}"
    return render(request, "frm-calendario.html", {"dias": dias, "horas": horas, "rango": rango, "week_offset": week_offset})


@login_required(login_url="signin")
def homeinpacientes(request):
    return render(request, "frm-pacientes.html")


@login_required(login_url="signin")
def homeinperfilpaciente(request):
    pacientes_demo = {
        "juan-smith": {"nombre": "Juan Smith", "edad": 45, "genero": "Masculino", "correo": "juan.smith@example.com", "estado": "Activo", "doctor": "Dr. Sarah Johnson"},
        "emily-davis": {"nombre": "Emily Davis", "edad": 32, "genero": "Femenino", "correo": "emily.davis@example.com", "estado": "Activo", "doctor": "Dr. Michael Chen"},
        "robert-wilson": {"nombre": "Robert Wilson", "edad": 58, "genero": "Masculino", "correo": "robert.wilson@example.com", "estado": "Inactivo", "doctor": "Dr. Lisa Patel"},
    }
    paciente_id = request.GET.get("paciente", "juan-smith")
    paciente = pacientes_demo.get(paciente_id, pacientes_demo["juan-smith"])
    return render(request, "frm-perfilpaciente.html", {"paciente": paciente})


@login_required(login_url="signin")
def homeineditarpaciente(request):
    pacientes_demo = {
        "juan-smith": {"nombre": "Juan Smith", "correo": "juan.smith@example.com", "genero": "Masculino", "estado": "Activo", "doctor": "Dr. Sarah Johnson"},
        "emily-davis": {"nombre": "Emily Davis", "correo": "emily.davis@example.com", "genero": "Femenino", "estado": "Activo", "doctor": "Dr. Michael Chen"},
        "robert-wilson": {"nombre": "Robert Wilson", "correo": "robert.wilson@example.com", "genero": "Masculino", "estado": "Inactivo", "doctor": "Dr. Lisa Patel"},
    }
    paciente_id = request.GET.get("paciente", "juan-smith")
    paciente = pacientes_demo.get(paciente_id, pacientes_demo["juan-smith"])
    return render(request, "frm-editarpaciente.html", {"paciente": paciente, "tipos_sangre": ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]})


@login_required(login_url="signin")
def homeinnuevopaciente(request):
    return render(request, "frm-nuevopaciente.html")


@login_required(login_url="signin")
def homeinnuevacita(request):
    return render(request, "frm-nuevacita.html", {"horas_demo": [f"{h:02d}:00" for h in range(8, 23)]})
