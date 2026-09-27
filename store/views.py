from datetime import date, timedelta
from functools import wraps
from pathlib import Path
import mimetypes

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.db import models
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import CitaForm, PacienteForm
from .models import Cita, DocumentoPaciente, Paciente, Post


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
    return render(request, "frm-menpri.html")


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
            models.Q(cedula__icontains=q)
            | models.Q(nombres__icontains=q)
            | models.Q(apellidos__icontains=q)
            | models.Q(correo__icontains=q)
            | models.Q(telefono__icontains=q)
        )
    if estado in {"ACTIVO", "INACTIVO"}:
        pacientes = pacientes.filter(estado=estado)
    return render(
        request,
        "frm-pacientes.html",
        {"pacientes": pacientes, "q": q, "estado": estado},
    )


@staff_required
def foto_paciente(request, paciente_id):
    paciente = get_object_or_404(Paciente, pk=paciente_id)
    if not paciente.foto_perfil:
        raise Http404("El paciente no tiene una foto de perfil.")

    try:
        archivo = paciente.foto_perfil.open("rb")
    except (FileNotFoundError, OSError):
        raise Http404("La foto de perfil no está disponible.")

    content_type = mimetypes.guess_type(paciente.foto_perfil.name)[0] or "application/octet-stream"
    return FileResponse(archivo, content_type=content_type)


@staff_required
def homeinperfilpaciente(request, paciente_id):
    paciente = get_object_or_404(
        Paciente.objects.select_related("profesional"),
        pk=paciente_id,
    )
    citas = paciente.citas.select_related("profesional").order_by("-fecha_hora")
    historias = paciente.historias_clinicas.select_related("profesional").order_by("-fecha")
    documentos = paciente.documentos.all()
    return render(
        request,
        "frm-perfilpaciente.html",
        {
            "paciente": paciente,
            "citas": citas,
            "historias": historias,
            "documentos": documentos,
        },
    )


@staff_required
def imprimir_perfil_paciente(request, paciente_id):
    paciente = get_object_or_404(Paciente.objects.select_related("profesional"), pk=paciente_id)
    citas = paciente.citas.select_related("profesional").order_by("-fecha_hora")
    documentos = paciente.documentos.all()
    return render(request, "perfil-paciente-imprimir.html", {
        "paciente": paciente,
        "citas": citas,
        "documentos": documentos,
    })


@staff_required
def cambiar_estado_paciente(request, paciente_id):
    paciente = get_object_or_404(Paciente, pk=paciente_id)

    if request.method != "POST":
        return redirect("homeinperfilpaciente", paciente_id=paciente.pk)

    if paciente.estado == "ACTIVO":
        paciente.estado = "INACTIVO"
        mensaje = f"El paciente {paciente.nombre} fue desactivado correctamente."
    else:
        paciente.estado = "ACTIVO"
        mensaje = f"El paciente {paciente.nombre} fue activado correctamente."

    paciente.save(update_fields=["estado", "actualizado_en"])
    messages.success(request, mensaje)
    return redirect("homeinpacientes")


@staff_required
def homeineditarpaciente(request, paciente_id):
    paciente = get_object_or_404(Paciente, pk=paciente_id)
    if request.method == "POST":
        form = PacienteForm(request.POST, request.FILES, instance=paciente)
        if form.is_valid():
            form.save()
            return redirect("homeinperfilpaciente", paciente_id=paciente.pk)
    else:
        form = PacienteForm(instance=paciente)
    return render(request, "frm-editarpaciente.html", {"form": form, "paciente": paciente})


@staff_required
def _guardar_documentos_subidos(request, paciente):
    campos_documentos = {
        "documento_consentimiento": "CONSENTIMIENTO_TRATAMIENTO",
        "documento_autorizacion": "AUTORIZACION_INFORMACION",
        "documento_identificacion": "IDENTIFICACION",
        "documento_otros": "OTRO",
    }

    for campo, tipo in campos_documentos.items():
        archivo = request.FILES.get(campo)
        if not archivo:
            continue

        extension = Path(archivo.name).suffix.lower()
        if extension not in {".pdf", ".jpg", ".jpeg", ".png"}:
            messages.error(
                request,
                f"El archivo {archivo.name} no tiene un formato permitido. "
                "Usa PDF, JPG, JPEG o PNG.",
            )
            continue

        if archivo.size > 10 * 1024 * 1024:
            messages.error(
                request,
                f"El archivo {archivo.name} supera el máximo permitido de 10 MB.",
            )
            continue

        DocumentoPaciente.objects.create(
            paciente=paciente,
            tipo=tipo,
            archivo=archivo,
            estado="FIRMADO",
        )


@staff_required
def homeinnuevopaciente(request):
    if request.method == "POST":
        form = PacienteForm(request.POST, request.FILES)
        if form.is_valid():
            paciente = form.save()
            _guardar_documentos_subidos(request, paciente)

            accion_documento = request.POST.get("accion_documento")
            if accion_documento in {
                "CONSENTIMIENTO_TRATAMIENTO",
                "AUTORIZACION_INFORMACION",
                "FICHA_ADMISION",
                "CONFIDENCIALIDAD",
                "AUTORIZACION_CONTACTO",
            }:
                return redirect(
                    "generar_documento_paciente",
                    paciente_id=paciente.pk,
                    tipo=accion_documento,
                )

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


@staff_required
def generar_documento_paciente(request, paciente_id, tipo):
    if tipo not in {
        "CONSENTIMIENTO_TRATAMIENTO",
        "AUTORIZACION_INFORMACION",
        "FICHA_ADMISION",
        "CONFIDENCIALIDAD",
        "AUTORIZACION_CONTACTO",
    }:
        raise Http404("Tipo de documento no válido.")

    paciente = get_object_or_404(Paciente.objects.select_related("profesional"), pk=paciente_id)

    return render(
        request,
        "documento-paciente-imprimir.html",
        {
            "paciente": paciente,
            "tipo": tipo,
            "fecha": date.today(),
        },
    )


@staff_required
def subir_documento_paciente(request, paciente_id):
    paciente = get_object_or_404(Paciente, pk=paciente_id)

    if request.method != "POST":
        return redirect("homeinperfilpaciente", paciente_id=paciente.pk)

    archivo = request.FILES.get("archivo")
    tipo = request.POST.get("tipo")

    tipos_validos = dict(DocumentoPaciente.TIPOS)
    if tipo not in tipos_validos:
        messages.error(request, "Tipo de documento no válido.")
        return redirect("homeinperfilpaciente", paciente_id=paciente.pk)

    if not archivo:
        messages.error(request, "Selecciona un archivo para cargar.")
        return redirect("homeinperfilpaciente", paciente_id=paciente.pk)

    extension = Path(archivo.name).suffix.lower()
    if extension not in {".pdf", ".jpg", ".jpeg", ".png"}:
        messages.error(request, "Solo se permiten archivos PDF, JPG, JPEG o PNG.")
        return redirect("homeinperfilpaciente", paciente_id=paciente.pk)

    if archivo.size > 10 * 1024 * 1024:
        messages.error(request, "El archivo supera el máximo permitido de 10 MB.")
        return redirect("homeinperfilpaciente", paciente_id=paciente.pk)

    DocumentoPaciente.objects.create(
        paciente=paciente,
        tipo=tipo,
        archivo=archivo,
        estado="FIRMADO",
    )
    messages.success(request, "Documento cargado correctamente.")
    return redirect("homeinperfilpaciente", paciente_id=paciente.pk)
