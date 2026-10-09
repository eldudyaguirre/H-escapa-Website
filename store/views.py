from datetime import date, timedelta
from functools import wraps
from pathlib import Path
import hashlib
import os
import mimetypes

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.db import models, transaction
from django.utils import timezone
from django.http import FileResponse, Http404
from django.core.mail import EmailMessage
from django.core.cache import cache
from django.contrib import messages
from .forms import AgendamientoForm, ContactoForm
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.templatetags.static import static

from .forms import CitaForm, EspecialidadForm, PacienteForm, ProfesionalForm, PostForm
from .models import Cita, CategoriaBlog, DocumentoPaciente, Especialidad, EtiquetaBlog, InteraccionWeb, InteraccionWebHistorial, Paciente, Post, Profesional



# Protección básica contra spam para los formularios públicos.
# Límite por IP y formulario: 3 envíos cada 60 minutos.
SPAM_MIN_SECONDS = 3
SPAM_MAX_AGE_SECONDS = 24 * 60 * 60
SPAM_MAX_SUBMISSIONS_PER_HOUR = 3


def _es_envio_spam(request, formulario):
    """Detecta honeypots, envíos demasiado rápidos y ráfagas por IP."""
    if request.method != "POST":
        return False

    # Los bots suelen rellenar todos los campos; este campo está oculto a personas.
    if request.POST.get("website", "").strip():
        return True

    try:
        iniciado = float(request.POST.get("form_started_at", ""))
    except (TypeError, ValueError):
        return True

    ahora = timezone.now().timestamp()
    transcurrido = ahora - iniciado
    if transcurrido < SPAM_MIN_SECONDS or transcurrido > SPAM_MAX_AGE_SECONDS:
        return True

    # No confiar en X-Forwarded-For recibido del cliente: puede falsificarse.
    ip = request.META.get("REMOTE_ADDR", "unknown")
    ip_hash = hashlib.sha256(ip.encode("utf-8")).hexdigest()[:32]
    clave = f"public-form-rate:{formulario}:{ip_hash}:{int(ahora // 3600)}"

    # cache.add crea el contador de forma atómica cuando todavía no existe.
    cache.add(clave, 0, timeout=3600)
    try:
        cantidad = cache.incr(clave)
    except ValueError:
        # Algunos backends pueden expirar la clave entre add e incr.
        cache.set(clave, 1, timeout=3600)
        cantidad = 1

    return cantidad > SPAM_MAX_SUBMISSIONS_PER_HOUR


def home(request):
    posts = (
        Post.objects.filter(estado="PUBLICADO")
        .select_related("categoria", "autor")
        .prefetch_related("etiquetas")
        .order_by("-fecha_publicacion", "-creado_en")[:3]
    )
    return render(request, "index.html", {"posts": posts})


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
def contactanos(request):
    form = ContactoForm(request.POST or None)

    if request.method == "POST" and _es_envio_spam(request, "contacto"):
        # Respuesta neutra para no indicar a los bots qué control los bloqueó.
        return redirect("contact")

    if request.method == "POST" and form.is_valid():
        recipient = os.getenv("CONTACT_FORM_RECIPIENT", "palaciohester@hotmail.com")
        sender = os.getenv("DEFAULT_FROM_EMAIL", os.getenv("EMAIL_HOST_USER"))
        nombres = form.cleaned_data["nombres"]
        apellidos = form.cleaned_data["apellidos"]
        telefono = form.cleaned_data["telefono"]
        correo = form.cleaned_data["email"]
        mensaje = form.cleaned_data["mensaje"]
        InteraccionWeb.objects.create(tipo="CONTACTO", nombres=nombres, apellidos=apellidos, email=correo, telefono=telefono, mensaje=mensaje)

        subject = f"H-Escapa | Nuevo mensaje de contacto de {nombres} {apellidos}"
        text_body = (
            f"Nombres: {nombres}\n"
            f"Apellidos: {apellidos}\n"
            f"Teléfono: {telefono}\n"
            f"Correo: {correo}\n\n"
            f"Mensaje:\n{mensaje}"
        )
        html_body = f"""
        <div style="margin:0;padding:0;background:#f3f7f6;font-family:Arial,Helvetica,sans-serif;color:#263b3a">
          <div style="max-width:680px;margin:30px auto;background:#ffffff;border-radius:16px;overflow:hidden;border:1px solid #dce9e6">
            <div style="background:#439b95;padding:28px 32px;text-align:center">
              <img src="https://www.h-escapa.com/static/img/logo-blanco.png" alt="H-Escapa" style="display:block;width:190px;height:auto;max-height:80px;object-fit:contain;margin:0 auto;">

            </div>
            <div style="padding:32px">
              <div style="font-size:12px;font-weight:700;color:#439b95;text-transform:uppercase;letter-spacing:1px">Contáctanos</div>
              <h1 style="margin:7px 0 8px;font-size:25px;color:#263b3a">Nuevo mensaje de contacto</h1>
              <p style="margin:0 0 25px;color:#758481;font-size:14px">Una persona ha enviado un mensaje desde el sitio web de H-Escapa.</p>
              
              <div style="background:#f5faf9;border:1px solid #e1ece9;border-radius:12px;padding:20px;margin-bottom:22px">
                <div style="font-size:12px;color:#7b8986;margin-bottom:5px">NOMBRE COMPLETO</div>
                <div style="font-size:17px;font-weight:600;color:#263b3a">{nombres} {apellidos}</div>
              </div>

              <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="margin-bottom:22px">
                <tr>
                  <td width="50%" style="padding:0 8px 0 0;vertical-align:top">
                    <div style="border:1px solid #e1e8e6;border-radius:10px;padding:15px">
                      <div style="font-size:11px;color:#87928f;margin-bottom:5px">TELÉFONO</div>
                      <div style="font-size:14px;color:#263b3a">{telefono}</div>
                    </div>
                  </td>
                  <td width="50%" style="padding:0 0 0 8px;vertical-align:top">
                    <div style="border:1px solid #e1e8e6;border-radius:10px;padding:15px">
                      <div style="font-size:11px;color:#87928f;margin-bottom:5px">CORREO ELECTRÓNICO</div>
                      <div style="font-size:14px;color:#263b3a;word-break:break-word">{correo}</div>
                    </div>
                  </td>
                </tr>
              </table>

              <div style="font-size:11px;color:#87928f;margin-bottom:8px">MENSAJE</div>
              <div style="background:#fafcfc;border-left:4px solid #439b95;border-radius:0 10px 10px 0;padding:18px 20px;color:#40504d;font-size:14px;line-height:1.65;white-space:pre-line">{mensaje}</div>

              <div style="margin-top:26px;text-align:center">
                <a href="mailto:{correo}" style="display:inline-block;background:#00615c;color:#ffffff;text-decoration:none;padding:12px 24px;border-radius:8px;font-size:14px;font-weight:600">Responder al usuario</a>
              </div>
            </div>
            <div style="background:#f5f8f7;padding:20px 32px;text-align:center;border-top:1px solid #e1e8e6">
              <div style="font-size:12px;color:#6f7d79">H-Escapa · Psicología y Salud Mental</div>
              <div style="font-size:12px;color:#87928f;margin-top:4px">Roberto Crespo 5-34 y Av 10 de Agosto · Cuenca, Ecuador</div>
            </div>
          </div>
        </div>
        """

        email = EmailMessage(
            subject=subject,
            body=text_body,
            from_email=sender,
            to=[recipient],
            reply_to=[correo],
        )
        email.content_subtype = "html"
        email.body = html_body
        email.send(fail_silently=False)
        messages.success(request, "Tu mensaje fue enviado correctamente. Te responderemos lo antes posible.", extra_tags="contact-form")
        return redirect("contact")

    return render(request, "contact.html", {
        "form": form,
        "form_started_at": timezone.now().timestamp(),
    })

def agendamiento(request):
    form = AgendamientoForm(request.POST or None)

    if request.method == "POST" and _es_envio_spam(request, "agendamiento"):
        messages.error(request, "No pudimos procesar la solicitud. Espera unos segundos, recarga la página e inténtalo nuevamente.", extra_tags="appointment-form")
        return render(request, "book-appointment.html", {
            "form": form,
            "form_started_at": timezone.now().timestamp(),
            "appointment_error": True,
        })

    if request.method == "POST":
        if form.is_valid():
            recipient = os.getenv("CONTACT_FORM_RECIPIENT", "palaciohester@hotmail.com")
            sender = os.getenv("DEFAULT_FROM_EMAIL", os.getenv("EMAIL_HOST_USER"))
            datos = form.cleaned_data

            InteraccionWeb.objects.create(tipo="AGENDAMIENTO", nombres=datos["nombres"], apellidos=datos["apellidos"], email=datos["email"], telefono=datos["telefono"], servicio=datos["servicio"], fecha_solicitada=datos["fecha"])

            subject = f"H-Escapa | Solicitud de cita - {datos['nombres']} {datos['apellidos']}"
            text_body = (
                f"Nombres: {datos['nombres']}\n"
                f"Apellidos: {datos['apellidos']}\n"
                f"Correo: {datos['email']}\n"
                f"Teléfono: {datos['telefono']}\n"
                f"Servicio: {datos['servicio']}\n"
                f"Fecha solicitada: {datos['fecha'].strftime('%d/%m/%Y')}\n"
            )
            html_body = f"""
            <div style="margin:0;padding:0;background:#f3f7f6;font-family:Arial,Helvetica,sans-serif;color:#263b3a">
              <div style="max-width:680px;margin:30px auto;background:#fff;border:1px solid #dce9e6;border-radius:16px;overflow:hidden">
                <div style="background:#439b95;padding:28px;text-align:center;color:#fff">
                  <div style="font-size:32px;font-weight:700">h<span style="font-weight:400">-escapa</span></div>
                  <div style="font-size:13px;color:#e8f7f5">Psicología y Salud Mental</div>
                </div>
                <div style="padding:32px">
                  <div style="font-size:12px;font-weight:700;color:#439b95;letter-spacing:1px;text-transform:uppercase">Agenda tu cita</div>
                  <h1 style="margin:7px 0 8px;font-size:25px">Nueva solicitud de cita</h1>
                  <p style="color:#758481;font-size:14px">Una persona ha solicitado una cita desde el sitio web.</p>
                  <div style="background:#f5faf9;border:1px solid #e1ece9;border-radius:12px;padding:20px;margin-top:24px">
                    <div style="font-size:12px;color:#7b8986">PACIENTE</div>
                    <div style="font-size:18px;font-weight:600;margin-top:5px">{datos['nombres']} {datos['apellidos']}</div>
                  </div>
                  <table width="100%" cellspacing="0" cellpadding="0" style="margin-top:18px">
                    <tr>
                      <td style="padding-right:8px"><div style="border:1px solid #e1e8e6;border-radius:10px;padding:15px"><small style="color:#87928f">TELÉFONO</small><div>{datos['telefono']}</div></div></td>
                      <td style="padding-left:8px"><div style="border:1px solid #e1e8e6;border-radius:10px;padding:15px"><small style="color:#87928f">CORREO</small><div style="word-break:break-word">{datos['email']}</div></div></td>
                    </tr>
                  </table>
                  <div style="margin-top:18px;padding:18px;background:#fafcfc;border-left:4px solid #439b95;border-radius:0 10px 10px 0">
                    <div><strong>Servicio:</strong> {datos['servicio']}</div>
                    <div style="margin-top:8px"><strong>Fecha solicitada:</strong> {datos['fecha'].strftime('%d/%m/%Y')}</div>
                  </div>
                  <div style="text-align:center;margin-top:25px"><a href="mailto:{datos['email']}" style="background:#00615c;color:#fff;text-decoration:none;padding:12px 24px;border-radius:8px;font-weight:600">Contactar al paciente</a></div>
                </div>
                <div style="background:#f5f8f7;padding:20px;text-align:center;font-size:12px;color:#6f7d79">H-Escapa · Psicología y Salud Mental<br>Roberto Crespo 5-34 y Av 10 de Agosto · Cuenca, Ecuador</div>
              </div>
            </div>
            """
            email = EmailMessage(subject=subject, body=text_body, from_email=sender, to=[recipient], reply_to=[datos["email"]])
            email.content_subtype = "html"
            email.body = html_body
            try:
                email.send(fail_silently=False)
            except Exception:
                messages.error(request, "No se pudo enviar la solicitud. Revisa la configuración del correo del servidor.", extra_tags="appointment-form")
            else:
                request.session["appointment_sent_confirmation"] = True
                return redirect("agendamiento")

    return render(request, "book-appointment.html", {
        "form": form,
        "form_started_at": timezone.now().timestamp(),
        "appointment_sent": request.session.pop("appointment_sent_confirmation", False),
    })


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
    imagen_url = request.build_absolute_uri(post.imagen_destacada.url) if post.imagen_destacada else request.build_absolute_uri(static("img/logo-blanco.png"))
    canonical_url = request.build_absolute_uri()
    return render(request, "blog-detalle-dinamico.html", {
        "post": post,
        "og_image": imagen_url,
        "canonical_url": canonical_url,
    })


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
@staff_required
def homein(request):
    hoy = timezone.localdate()
    inicio_hoy = timezone.make_aware(timezone.datetime.combine(hoy, timezone.datetime.min.time()))
    fin_hoy = inicio_hoy + timedelta(days=1)

    citas_hoy = (
        Cita.objects
        .select_related("paciente", "profesional")
        .filter(fecha_hora__gte=inicio_hoy, fecha_hora__lt=fin_hoy)
        .exclude(estado__in=["CANCELADA", "NO_ASISTIO"])
        .order_by("fecha_hora")
    )

    pacientes_activos = Paciente.objects.filter(estado="ACTIVO").count()
    profesionales_activos = Profesional.objects.filter(activo=True).count()
    posts_publicados = Post.objects.filter(estado="PUBLICADO").count()
    solicitudes_web_pendientes = InteraccionWeb.objects.filter(estado="PENDIENTE").count()
    solicitudes_web_contacto = InteraccionWeb.objects.filter(tipo="CONTACTO").count()
    solicitudes_web_agendamiento = InteraccionWeb.objects.filter(tipo="AGENDAMIENTO").count()

    pacientes_recientes = Paciente.objects.order_by("-creado_en")[:3]
    profesionales_recientes = Profesional.objects.select_related("especialidad").order_by("-creado_en")[:3]
    citas_proximas = (
        Cita.objects
        .select_related("paciente", "profesional")
        .filter(fecha_hora__gte=timezone.now())
        .exclude(estado__in=["CANCELADA", "NO_ASISTIO"])
        .order_by("fecha_hora")[:5]
    )

    return render(request, "frm-menpri.html", {
        "citas_hoy": citas_hoy,
        "citas_hoy_count": citas_hoy.count(),
        "pacientes_activos": pacientes_activos,
        "profesionales_activos": profesionales_activos,
        "posts_publicados": posts_publicados,
        "solicitudes_web_pendientes": solicitudes_web_pendientes,
        "solicitudes_web_contacto": solicitudes_web_contacto,
        "solicitudes_web_agendamiento": solicitudes_web_agendamiento,
        "pacientes_recientes": pacientes_recientes,
        "profesionales_recientes": profesionales_recientes,
        "citas_proximas": citas_proximas,
        "fecha_hoy": hoy,
    })


@staff_required
def homeincalendario(request):
    citas = Cita.objects.select_related("paciente", "profesional").order_by("fecha_hora")
    return render(request, "frm-calendario.html", {"citas": citas})




@staff_required
def homeinespecialidades(request):
    especialidades = Especialidad.objects.all()
    q = request.GET.get("q", "").strip()
    estado = request.GET.get("estado", "").strip()

    if q:
        especialidades = especialidades.filter(nombre__icontains=q)
    if estado == "ACTIVA":
        especialidades = especialidades.filter(activa=True)
    elif estado == "INACTIVA":
        especialidades = especialidades.filter(activa=False)

    total = Especialidad.objects.count()
    activas = Especialidad.objects.filter(activa=True).count()
    inactivas = Especialidad.objects.filter(activa=False).count()
    total_profesionales = Profesional.objects.count()
    profesionales_asignados = Profesional.objects.filter(especialidad__isnull=False).count()

    return render(request, "frm-especialidades.html", {
        "especialidades": especialidades,
        "q": q,
        "estado": estado,
        "total": total,
        "activas": activas,
        "inactivas": inactivas,
        "total_profesionales": total_profesionales,
        "profesionales_asignados": profesionales_asignados,
    })


@staff_required
def homeineditarespecialidad(request, especialidad_id):
    especialidad = get_object_or_404(Especialidad, pk=especialidad_id)

    if request.method == "POST":
        form = EspecialidadForm(request.POST, instance=especialidad)
        if form.is_valid():
            form.save()
            messages.success(request, f"Especialidad «{especialidad.nombre}» actualizada correctamente.")
            return redirect("homeinespecialidades")
    else:
        form = EspecialidadForm(instance=especialidad)

    return render(request, "frm-nuevaespecialidad.html", {
        "form": form,
        "editar": True,
        "especialidad": especialidad,
    })


@staff_required
def cambiar_estado_especialidad(request, especialidad_id):
    especialidad = get_object_or_404(Especialidad, pk=especialidad_id)

    if request.method != "POST":
        return redirect("homeinespecialidades")

    especialidad.activa = not especialidad.activa
    especialidad.save(update_fields=["activa", "actualizado_en"])
    estado = "activada" if especialidad.activa else "desactivada"
    messages.success(request, f"Especialidad «{especialidad.nombre}» {estado} correctamente.")
    return redirect("homeinespecialidades")


@staff_required
def homeinnuevaespecialidad(request):
    if request.method == "POST":
        form = EspecialidadForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Especialidad creada correctamente.")
            return redirect("homeinespecialidades")
    else:
        form = EspecialidadForm()
    return render(request, "frm-nuevaespecialidad.html", {"form": form})


@staff_required
def homeinnuevoprofesional(request):
    if request.method == "POST":
        form = ProfesionalForm(request.POST, request.FILES)
        if form.is_valid():
            with transaction.atomic():
                User = get_user_model()
                usuario = User.objects.create_user(
                    username=form.cleaned_data["username"],
                    email=form.cleaned_data["email"],
                    password=form.cleaned_data["password1"],
                    is_active=form.cleaned_data["activo"],
                    is_staff=True,
                )
                Profesional.objects.create(
                    usuario=usuario,
                    foto=form.cleaned_data.get("foto"),
                    cedula=form.cleaned_data.get("cedula", "").strip(),
                    nombre=form.cleaned_data["nombre"].strip(),
                    apellido=form.cleaned_data["apellido"].strip(),
                    fecha_nacimiento=form.cleaned_data.get("fecha_nacimiento"),
                    genero=form.cleaned_data.get("genero", ""),
                    telefono=form.cleaned_data.get("telefono", "").strip(),
                    direccion=form.cleaned_data.get("direccion", "").strip(),
                    ciudad=form.cleaned_data.get("ciudad", "").strip(),
                    provincia=form.cleaned_data.get("provincia", "").strip(),
                    codigo_postal=form.cleaned_data.get("codigo_postal", "").strip(),
                    pais=form.cleaned_data.get("pais", "Ecuador").strip(),
                    contacto_emergencia_nombre=form.cleaned_data.get("contacto_emergencia_nombre", "").strip(),
                    contacto_emergencia_telefono=form.cleaned_data.get("contacto_emergencia_telefono", "").strip(),
                    contacto_emergencia_relacion=form.cleaned_data.get("contacto_emergencia_relacion", "").strip(),
                    profesion=form.cleaned_data.get("profesion", "").strip(),
                    especialidad=form.cleaned_data["especialidad"],
                    especializacion=form.cleaned_data.get("especializacion", "").strip(),
                    titulo=form.cleaned_data.get("titulo", "").strip(),
                    institucion_titulo=form.cleaned_data.get("institucion_titulo", "").strip(),
                    anio_titulo=form.cleaned_data.get("anio_titulo"),
                    tipo_licencia=form.cleaned_data.get("tipo_licencia", "").strip(),
                    numero_licencia=form.cleaned_data.get("numero_licencia", "").strip(),
                    fecha_emision_licencia=form.cleaned_data.get("fecha_emision_licencia"),
                    fecha_vencimiento_licencia=form.cleaned_data.get("fecha_vencimiento_licencia"),
                    biografia=form.cleaned_data.get("biografia", "").strip(),
                    codigo_empleado=form.cleaned_data.get("codigo_empleado", "").strip(),
                    tipo_contrato=form.cleaned_data.get("tipo_contrato", ""),
                    fecha_ingreso=form.cleaned_data.get("fecha_ingreso"),
                    activo=form.cleaned_data["activo"],
                    forzar_cambio_clave=form.cleaned_data["forzar_cambio_clave"],
                    dos_factores=form.cleaned_data["dos_factores"],
                )
                # Crear/asignar el grupo correspondiente al rol del sistema.
                role = form.cleaned_data.get("rol_sistema", "PROFESIONAL")
                role_names = {
                    "ADMINISTRADOR": "Administradores",
                    "GESTOR": "Gestores",
                    "PROFESIONAL": "Profesionales",
                    "RECEPCION": "Recepción",
                    "PERSONAL": "Personal",
                }
                group, _ = Group.objects.get_or_create(name=role_names[role])

                # Aplicar permisos Django seleccionados desde la pestaña Acceso y cuenta.
                permisos = form.cleaned_data.get("permisos", [])
                permission_map = {
                    "pacientes": "paciente",
                    "citas": "cita",
                    "profesionales": "profesional",
                }
                selected_permissions = []
                for key in permisos:
                    modulo, accion = key.rsplit("_", 1)
                    model_name = permission_map.get(modulo)
                    if model_name:
                        permiso = Permission.objects.filter(
                            content_type__app_label="store",
                            content_type__model=model_name,
                            codename=f"{accion}_{model_name}",
                        ).first()
                        if permiso:
                            selected_permissions.append(permiso)
                usuario.user_permissions.set(selected_permissions)
                group.permissions.set(selected_permissions)
                usuario.groups.set([group])
            messages.success(request, f"Profesional {form.cleaned_data['nombre']} {form.cleaned_data['apellido']} creado correctamente.")
            return redirect("homeinprofesionales")
    else:
        form = ProfesionalForm()
    return render(request, "frm-nuevoprofesional.html", {"form": form})


@staff_required
def homeinprofesionales(request):
    profesionales = Profesional.objects.select_related("usuario").all()
    q = request.GET.get("q", "").strip()
    estado = request.GET.get("estado", "").strip()
    especialidad = request.GET.get("especialidad", "").strip()

    if q:
        profesionales = profesionales.filter(
            models.Q(nombre__icontains=q)
            | models.Q(apellido__icontains=q)
            | models.Q(telefono__icontains=q)
            | models.Q(usuario__username__icontains=q)
            | models.Q(usuario__email__icontains=q)
        )

    if estado == "ACTIVO":
        profesionales = profesionales.filter(activo=True)
    elif estado == "INACTIVO":
        profesionales = profesionales.filter(activo=False)

    if especialidad:
        profesionales = profesionales.filter(especialidad=especialidad)

    total_profesionales = Profesional.objects.count()
    activos = Profesional.objects.filter(activo=True).count()
    inactivos = Profesional.objects.filter(activo=False).count()

    especialidades = [
        {"nombre": especialidad.nombre, "cantidad": especialidad.profesionales.count()}
        for especialidad in Especialidad.objects.filter(activa=True)
    ]

    return render(
        request,
        "frm-profesionales.html",
        {
            "profesionales": profesionales,
            "q": q,
            "estado": estado,
            "especialidad": especialidad,
            "especialidades_opciones": Especialidad.objects.filter(activa=True),
            "total_profesionales": total_profesionales,
            "activos": activos,
            "inactivos": inactivos,
            "especialidades": especialidades,
        },
    )


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


@staff_required
def homeinblog(request):
    posts = Post.objects.select_related("autor", "categoria").prefetch_related("etiquetas").all()
    estado = request.GET.get("estado", "").strip()
    q = request.GET.get("q", "").strip()

    if estado in {"BORRADOR", "PUBLICADO", "ARCHIVADO"}:
        posts = posts.filter(estado=estado)
    if q:
        posts = posts.filter(
            models.Q(titulo__icontains=q)
            | models.Q(resumen__icontains=q)
            | models.Q(contenido__icontains=q)
        )

    return render(request, "frm-blog.html", {
        "posts": posts,
        "estado": estado,
        "q": q,
        "total_posts": Post.objects.count(),
        "publicados": Post.objects.filter(estado="PUBLICADO").count(),
        "borradores": Post.objects.filter(estado="BORRADOR").count(),
        "archivados": Post.objects.filter(estado="ARCHIVADO").count(),
        "active_menu": "blog",
    })


@staff_required
def homeinnuevopost(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.autor = request.user
            if not post.autor_nombre:
                post.autor_nombre = request.user.get_full_name().strip() or request.user.get_username()
            post.save()
            form.save_m2m()
            messages.success(request, "Publicación guardada correctamente.")
            return redirect("homeinblog")
    else:
        form = PostForm(initial={
            "autor_nombre": request.user.get_full_name().strip() or request.user.get_username(),
        })
    return render(request, "frm-nuevopost.html", {
        "form": form,
        "editar": False,
        "active_menu": "blog",
    })


@staff_required
def homeineditarpost(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            if not post.autor_id:
                post.autor = request.user
            post.save()
            form.save_m2m()
            messages.success(request, "Publicación actualizada correctamente.")
            return redirect("homeinblog")
    else:
        form = PostForm(instance=post)
    return render(request, "frm-nuevopost.html", {
        "form": form,
        "editar": True,
        "post": post,
        "active_menu": "blog",
    })


@staff_required
def eliminarpost(request, post_id):
    if request.method != "POST":
        return redirect("homeinblog")
    post = get_object_or_404(Post, pk=post_id)
    titulo = post.titulo
    post.delete()
    messages.success(request, f"El post «{titulo}» fue eliminado.")
    return redirect("homeinblog")


@staff_required
def cambiar_estado_post(request, post_id):
    if request.method != "POST":
        return redirect("homeinblog")
    post = get_object_or_404(Post, pk=post_id)
    nuevo_estado = request.POST.get("estado", "")
    if nuevo_estado not in dict(Post.ESTADOS):
        messages.error(request, "Estado de publicación no válido.")
        return redirect("homeinblog")
    post.estado = nuevo_estado
    post.save()
    messages.success(request, f"El post «{post.titulo}» ahora está {post.get_estado_display().lower()}.")
    return redirect("homeinblog")


@staff_required
def homeininteraccionesweb(request):
    interacciones = InteraccionWeb.objects.all()
    tipo = request.GET.get("tipo", "").strip()
    estado = request.GET.get("estado", "").strip()
    q = request.GET.get("q", "").strip()
    if tipo:
        interacciones = interacciones.filter(tipo=tipo)
    if estado:
        interacciones = interacciones.filter(estado=estado)
    if q:
        interacciones = interacciones.filter(
            models.Q(nombres__icontains=q) |
            models.Q(apellidos__icontains=q) |
            models.Q(email__icontains=q) |
            models.Q(telefono__icontains=q)
        )
    return render(request, "frm-interaccionesweb.html", {
        "interacciones": interacciones,
        "tipo": tipo,
        "estado": estado,
        "q": q,
        "total": InteraccionWeb.objects.count(),
        "pendientes": InteraccionWeb.objects.filter(estado="PENDIENTE").count(),
        "contactos": InteraccionWeb.objects.filter(tipo="CONTACTO").count(),
        "agendamientos": InteraccionWeb.objects.filter(tipo="AGENDAMIENTO").count(),
    })


@staff_required
def homeininteraccionweb(request, interaccion_id):
    interaccion = get_object_or_404(InteraccionWeb, pk=interaccion_id)
    if request.method == "POST":
        nuevo_estado = request.POST.get("estado", "").strip()
        comentario = request.POST.get("comentario", "").strip()
        if nuevo_estado in dict(InteraccionWeb.ESTADOS):
            anterior = interaccion.estado
            if nuevo_estado != anterior or comentario:
                interaccion.estado = nuevo_estado
                if comentario:
                    interaccion.observaciones = comentario
                interaccion.save(update_fields=["estado", "observaciones", "actualizado_en"])
                InteraccionWebHistorial.objects.create(interaccion=interaccion, estado_anterior=anterior, estado_nuevo=nuevo_estado, comentario=comentario, usuario=request.user)
                messages.success(request, "Seguimiento actualizado correctamente.")
        return redirect("homeininteraccionweb", interaccion_id=interaccion.id)
    return render(request, "frm-interaccionweb-detalle.html", {"interaccion": interaccion, "historial": interaccion.historial.all()})


