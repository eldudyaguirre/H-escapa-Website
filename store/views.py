from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import get_object_or_404, redirect, render
from django.db import models
from django.urls import reverse
from django.utils import timezone
from datetime import date, timedelta

from .forms import CitaForm, PacienteForm
from .models import Cita, HistoriaClinica, Paciente, Post
from functools import wraps


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



def staff_required(view_func):
    """Permite el acceso al panel interno únicamente a usuarios activos del personal."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(f"{reverse('signin')}?next={request.path}")
        if not request.user.is_active or not request.user.is_staff:
            return redirect("home")
        return view_func(request, *args, **kwargs)
    return wrapper


@staff_required
def homein(request):
    hoy = timezone.localdate()

    # Indicadores reales del consultorio.
    citas_hoy = (
        Cita.objects.filter(fecha_hora__date=hoy)
        .select_related("paciente", "profesional")
        .order_by("fecha_hora")
    )
    pacientes_activos = Paciente.objects.filter(estado="ACTIVO").count()
    historias_clinicas = HistoriaClinica.objects.count()
    posts_publicados = Post.objects.filter(estado="PUBLICADO").count()

    # Agenda de hoy.
    agenda = []
    for cita in citas_hoy:
        estado_label = dict(Cita.ESTADOS).get(cita.estado, cita.estado)
        estado_clase = "pending" if cita.estado == "PROGRAMADA" else ""
        if cita.modalidad == "VIRTUAL":
            estado_clase = "online"
        agenda.append({
            "hora": cita.fecha_hora.strftime("%H:%M"),
            "paciente": str(cita.paciente),
            "estado": estado_label,
            "estado_clase": estado_clase,
        })

    # Actividad reciente basada en registros reales.
    actividad = []

    for paciente in Paciente.objects.order_by("-creado_en")[:5]:
        actividad.append({
            "fecha": paciente.creado_en,
            "icono": "bx-user-plus",
            "texto": f"Paciente {paciente} registrado",
        })

    for historia in (
        HistoriaClinica.objects.select_related("paciente")
        .order_by("-creado_en")[:5]
    ):
        actividad.append({
            "fecha": historia.creado_en,
            "icono": "bx-file",
            "texto": f"Historia clínica registrada para {historia.paciente}",
        })

    for post in (
        Post.objects.filter(estado="PUBLICADO")
        .order_by("-fecha_publicacion", "-creado_en")[:5]
    ):
        actividad.append({
            "fecha": post.fecha_publicacion or post.creado_en,
            "icono": "bx-edit-alt",
            "texto": f'Post "{post.titulo}" publicado',
        })

    for cita in Cita.objects.select_related("paciente").order_by("-creado_en")[:5]:
        actividad.append({
            "fecha": cita.creado_en,
            "icono": "bx-calendar-event",
            "texto": f"Cita registrada para {cita.paciente}",
        })

    actividad.sort(key=lambda item: item["fecha"], reverse=True)
    actividad = actividad[:5]

    # Resumen real de citas de la semana.
    inicio_semana = hoy - timedelta(days=hoy.weekday())
    fin_semana = inicio_semana + timedelta(days=6)
    citas_semana = (
        Cita.objects.filter(fecha_hora__date__range=(inicio_semana, fin_semana))
        .values_list("fecha_hora", flat=True)
    )
    citas_por_dia = {}
    for fecha_hora in citas_semana:
        dia = timezone.localtime(fecha_hora).date() if timezone.is_aware(fecha_hora) else fecha_hora.date()
        citas_por_dia[dia] = citas_por_dia.get(dia, 0) + 1

    nombres_dias = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
    semana = [
        {
            "nombre": nombres_dias[i],
            "fecha": inicio_semana + timedelta(days=i),
            "cantidad": citas_por_dia.get(inicio_semana + timedelta(days=i), 0),
            "hoy": inicio_semana + timedelta(days=i) == hoy,
        }
        for i in range(7)
    ]

    contexto = {
        "citas_hoy": citas_hoy.count(),
        "pacientes_activos": pacientes_activos,
        "historias_clinicas": historias_clinicas,
        "posts_publicados": posts_publicados,
        "agenda": agenda,
        "actividad": actividad,
        "semana": semana,
        "fecha_hoy": hoy,
    }
    return render(request, "frm-menpri.html", contexto)


@staff_required
def homeincalendario(request):
    citas = Cita.objects.select_related("paciente", "profesional").order_by("fecha_hora")
    return render(request, "frm-calendario.html", {"citas": citas})


@staff_required
def homeinpacientes(request):
    pacientes = Paciente.objects.select_related("profesional").all()
    q = request.GET.get("q", "").strip()
    estado = request.GET.get("estado", "").strip()
    if q:
        pacientes = pacientes.filter(
            models.Q(nombres__icontains=q) |
            models.Q(apellidos__icontains=q) |
            models.Q(correo__icontains=q) |
            models.Q(telefono__icontains=q)
        )
    if estado in {"ACTIVO", "INACTIVO"}:
        pacientes = pacientes.filter(estado=estado)
    return render(request, "frm-pacientes.html", {"pacientes": pacientes, "q": q, "estado": estado})


@staff_required
def homeinperfilpaciente(request, paciente_id):
    paciente = get_object_or_404(Paciente.objects.select_related("profesional"), pk=paciente_id)
    citas = paciente.citas.select_related("profesional").order_by("-fecha_hora")
    historias = paciente.historias_clinicas.select_related("profesional").order_by("-fecha")
    return render(request, "frm-perfilpaciente.html", {"paciente": paciente, "citas": citas, "historias": historias})


@staff_required
def homeineditarpaciente(request, paciente_id):
    paciente = get_object_or_404(Paciente, pk=paciente_id)
    if request.method == "POST":
        form = PacienteForm(request.POST, instance=paciente)
        if form.is_valid():
            form.save()
            return redirect("homeinperfilpaciente", paciente_id=paciente.pk)
    else:
        form = PacienteForm(instance=paciente)
    return render(request, "frm-editarpaciente.html", {"form": form, "paciente": paciente})


@staff_required
def homeinnuevopaciente(request):
    if request.method == "POST":
        form = PacienteForm(request.POST)
        if form.is_valid():
            paciente = form.save()
            return redirect("homeinperfilpaciente", paciente_id=paciente.pk)
    else:
        form = PacienteForm()
    return render(request, "frm-nuevopaciente.html", {"form": form})


@staff_required
def homeinnuevacita(request):
    if request.method == "POST":
        form = CitaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("homeincalendario")
    else:
        initial = {}
        paciente_id = request.GET.get("paciente")
        if paciente_id:
            initial["paciente"] = paciente_id
        form = CitaForm(initial=initial)
    return render(request, "frm-nuevacita.html", {"form": form})
