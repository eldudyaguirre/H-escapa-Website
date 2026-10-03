from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from PIL import Image, ImageOps
from io import BytesIO
from django.core.files.base import ContentFile


class Especialidad(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    activa = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["nombre"]
        verbose_name = "Especialidad"
        verbose_name_plural = "Especialidades"

    def __str__(self):
        return self.nombre


class Profesional(models.Model):
    GENEROS = [
        ("M", "Masculino"), ("F", "Femenino"), ("O", "Otro"), ("N", "Prefiero no indicar"),
    ]
    TIPOS_CONTRATO = [
        ("TIEMPO_COMPLETO", "Tiempo completo"), ("MEDIO_TIEMPO", "Medio tiempo"),
        ("CONTRATO", "Contrato"), ("TEMPORAL", "Temporal"), ("PRACTICAS", "Prácticas"),
    ]

    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profesional")

    foto = models.ImageField(upload_to="profesionales/fotos/", blank=True, null=True)
    cedula = models.CharField(max_length=10, blank=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    genero = models.CharField(max_length=1, choices=GENEROS, blank=True)
    telefono = models.CharField(max_length=30, blank=True)
    direccion = models.CharField(max_length=250, blank=True)
    ciudad = models.CharField(max_length=100, blank=True)
    provincia = models.CharField(max_length=100, blank=True)
    codigo_postal = models.CharField(max_length=20, blank=True)
    pais = models.CharField(max_length=100, default="Ecuador", blank=True)
    contacto_emergencia_nombre = models.CharField(max_length=150, blank=True)
    contacto_emergencia_telefono = models.CharField(max_length=30, blank=True)
    contacto_emergencia_relacion = models.CharField(max_length=80, blank=True)

    profesion = models.CharField(max_length=150, blank=True)
    especialidad = models.ForeignKey(Especialidad, on_delete=models.PROTECT, related_name="profesionales")
    especializacion = models.CharField(max_length=150, blank=True)
    titulo = models.CharField(max_length=150, blank=True)
    institucion_titulo = models.CharField(max_length=200, blank=True)
    anio_titulo = models.PositiveIntegerField(blank=True, null=True)
    tipo_licencia = models.CharField(max_length=150, blank=True)
    numero_licencia = models.CharField(max_length=100, blank=True)
    fecha_emision_licencia = models.DateField(blank=True, null=True)
    fecha_vencimiento_licencia = models.DateField(blank=True, null=True)
    biografia = models.TextField(blank=True)

    codigo_empleado = models.CharField(max_length=50, blank=True)
    tipo_contrato = models.CharField(max_length=20, choices=TIPOS_CONTRATO, blank=True)
    fecha_ingreso = models.DateField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    forzar_cambio_clave = models.BooleanField(default=True)
    dos_factores = models.BooleanField(default=False)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["apellido", "nombre"]
        verbose_name = "Profesional"
        verbose_name_plural = "Profesionales"

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Paciente(models.Model):
    GENEROS = [
        ("F", "Femenino"),
        ("M", "Masculino"),
        ("O", "Otro"),
        ("N", "Prefiero no indicar"),
    ]

    ESTADOS = [
        ("ACTIVO", "Activo"),
        ("INACTIVO", "Inactivo"),
    ]

    TIPOS_SANGRE = [
        ("A+", "A+"),
        ("A-", "A-"),
        ("B+", "B+"),
        ("B-", "B-"),
        ("AB+", "AB+"),
        ("AB-", "AB-"),
        ("O+", "O+"),
        ("O-", "O-"),
        ("ND", "No determinado"),
    ]

    cedula = models.CharField(max_length=10, primary_key=True)
    foto_perfil = models.ImageField(upload_to="pacientes/fotos/", blank=True, null=True)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    genero = models.CharField(max_length=1, choices=GENEROS, blank=True)
    correo = models.EmailField(blank=True)
    telefono = models.CharField(max_length=30, blank=True)
    telefono_alternativo = models.CharField(max_length=30, blank=True)
    direccion = models.CharField(max_length=250, blank=True)
    ciudad = models.CharField(max_length=100, blank=True)
    provincia = models.CharField(max_length=100, blank=True)
    codigo_postal = models.CharField(max_length=20, blank=True)
    estado_civil = models.CharField(max_length=20, blank=True)
    contacto_preferido = models.CharField(max_length=10, default="telefono", blank=True)
    recibir_recordatorios_citas = models.BooleanField(default=False)
    recibir_notificaciones_resultados = models.BooleanField(default=False)
    recibir_notificaciones_recetas = models.BooleanField(default=False)
    recibir_boletin_novedades = models.BooleanField(default=False)
    tipo_sangre = models.CharField(max_length=3, choices=TIPOS_SANGRE, default="ND")
    altura_cm = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    peso_kg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    alergias = models.TextField(blank=True)
    medicamentos_actuales = models.TextField(blank=True)
    condiciones_cronicas = models.TextField(blank=True)
    cirugias_previas = models.TextField(blank=True)
    hospitalizaciones = models.TextField(blank=True)
    antecedentes_familiares = models.TextField(blank=True)
    tabaquismo = models.CharField(max_length=10, blank=True)
    consumo_alcohol = models.CharField(max_length=15, blank=True)
    consumo_drogas = models.CharField(max_length=15, blank=True)
    frecuencia_ejercicio = models.CharField(max_length=15, blank=True)
    habitos_dieteticos = models.TextField(blank=True)
    contacto_emergencia = models.CharField(max_length=150, blank=True)
    relacion_emergencia = models.CharField(max_length=80, blank=True)
    telefono_emergencia = models.CharField(max_length=30, blank=True)
    correo_emergencia = models.EmailField(blank=True)
    seguro_proveedor = models.CharField(max_length=150, blank=True)
    seguro_poliza = models.CharField(max_length=100, blank=True)
    seguro_grupo = models.CharField(max_length=100, blank=True)
    seguro_titular = models.CharField(max_length=150, blank=True)
    seguro_relacion = models.CharField(max_length=30, blank=True)
    seguro_telefono = models.CharField(max_length=30, blank=True)
    seguro_secundario = models.BooleanField(default=False)
    seguro_secundario_proveedor = models.CharField(max_length=150, blank=True)
    seguro_secundario_poliza = models.CharField(max_length=100, blank=True)
    tipo_identificacion_facturacion = models.CharField(max_length=20, blank=True)
    identificacion_facturacion = models.CharField(max_length=13, blank=True)
    nombre_facturacion = models.CharField(max_length=200, blank=True)
    correo_facturacion = models.EmailField(blank=True)
    metodo_facturacion = models.CharField(max_length=20, blank=True)
    pago_efectivo = models.BooleanField(default=False)
    pago_tarjeta = models.BooleanField(default=False)
    pago_transferencia = models.BooleanField(default=False)
    pago_deposito = models.BooleanField(default=False)
    pago_cheque = models.BooleanField(default=False)
    pago_otros = models.BooleanField(default=False)
    pago_online = models.BooleanField(default=False)
    profesional = models.ForeignKey(
        Profesional,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="pacientes",
    )
    estado = models.CharField(max_length=10, choices=ESTADOS, default="ACTIVO")
    observaciones = models.TextField(blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["apellidos", "nombres"]
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"
        indexes = [
            models.Index(fields=["apellidos", "nombres"]),
            models.Index(fields=["estado"]),
        ]

    @property
    def nombre(self):
        return f"{self.nombres} {self.apellidos}"

    @property
    def edad(self):
        if not self.fecha_nacimiento:
            return None
        hoy = timezone.localdate()
        return hoy.year - self.fecha_nacimiento.year - (
            (hoy.month, hoy.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day)
        )

    @property
    def doctor(self):
        return str(self.profesional) if self.profesional else "Sin asignar"

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"


class Cita(models.Model):
    ESTADOS = [
        ("PROGRAMADA", "Programada"),
        ("CONFIRMADA", "Confirmada"),
        ("ATENDIDA", "Atendida"),
        ("CANCELADA", "Cancelada"),
        ("NO_ASISTIO", "No asistió"),
    ]

    MODALIDADES = [
        ("PRESENCIAL", "Presencial"),
        ("VIRTUAL", "Virtual"),
    ]

    paciente = models.ForeignKey(Paciente, on_delete=models.PROTECT, related_name="citas")
    profesional = models.ForeignKey(Profesional, on_delete=models.PROTECT, related_name="citas")
    fecha_hora = models.DateTimeField()
    duracion_minutos = models.PositiveIntegerField(default=60)
    modalidad = models.CharField(max_length=12, choices=MODALIDADES, default="PRESENCIAL")
    estado = models.CharField(max_length=12, choices=ESTADOS, default="PROGRAMADA")
    motivo = models.CharField(max_length=250, blank=True)
    notas = models.TextField(blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["fecha_hora"]
        verbose_name = "Cita"
        verbose_name_plural = "Citas"
        indexes = [
            models.Index(fields=["fecha_hora"]),
            models.Index(fields=["profesional", "fecha_hora"]),
            models.Index(fields=["paciente", "fecha_hora"]),
        ]

    def __str__(self):
        return f"{self.paciente} - {self.fecha_hora:%d/%m/%Y %H:%M}"


class HistoriaClinica(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name="historias_clinicas")
    profesional = models.ForeignKey(Profesional, on_delete=models.PROTECT, related_name="historias_clinicas")
    cita = models.ForeignKey(Cita, on_delete=models.SET_NULL, null=True, blank=True, related_name="registros_clinicos")
    fecha = models.DateTimeField(default=timezone.now)
    motivo_consulta = models.TextField(blank=True)
    evaluacion = models.TextField(blank=True)
    diagnostico = models.TextField(blank=True)
    intervencion = models.TextField(blank=True)
    observaciones = models.TextField(blank=True)
    plan_seguimiento = models.TextField(blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-fecha"]
        verbose_name = "Historia clínica"
        verbose_name_plural = "Historias clínicas"
        indexes = [
            models.Index(fields=["paciente", "-fecha"]),
        ]

    def __str__(self):
        return f"{self.paciente} - {self.fecha:%d/%m/%Y}"


class DocumentoPaciente(models.Model):
    TIPOS = [
        ("CONSENTIMIENTO_TRATAMIENTO", "Consentimiento para tratamiento"),
        ("AUTORIZACION_INFORMACION", "Autorización de información"),
        ("FICHA_ADMISION", "Ficha de admisión"),
        ("CONFIDENCIALIDAD", "Compromiso de confidencialidad"),
        ("AUTORIZACION_CONTACTO", "Autorización de contacto"),
        ("IDENTIFICACION", "Documento de identificación"),
        ("OTRO", "Otros documentos"),
    ]

    ESTADOS = [
        ("PENDIENTE", "Pendiente de firma"),
        ("FIRMADO", "Firmado y cargado"),
    ]

    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        related_name="documentos",
    )
    tipo = models.CharField(max_length=40, choices=TIPOS)
    archivo = models.FileField(upload_to="pacientes/documentos/")
    estado = models.CharField(max_length=10, choices=ESTADOS, default="FIRMADO")
    observaciones = models.TextField(blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-creado_en"]
        verbose_name = "Documento del paciente"
        verbose_name_plural = "Documentos del paciente"
        indexes = [
            models.Index(fields=["paciente", "tipo"]),
            models.Index(fields=["paciente", "-creado_en"]),
        ]

    def __str__(self):
        return f"{self.paciente} - {self.get_tipo_display()}"


class CategoriaBlog(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    descripcion = models.TextField(blank=True)
    activa = models.BooleanField(default=True)

    class Meta:
        ordering = ["nombre"]
        verbose_name = "Categoría del blog"
        verbose_name_plural = "Categorías del blog"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre


class EtiquetaBlog(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=60, unique=True, blank=True)

    class Meta:
        ordering = ["nombre"]
        verbose_name = "Etiqueta del blog"
        verbose_name_plural = "Etiquetas del blog"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre


class Post(models.Model):
    ESTADOS = [
        ("BORRADOR", "Borrador"),
        ("PUBLICADO", "Publicado"),
        ("ARCHIVADO", "Archivado"),
    ]

    titulo = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    resumen = models.TextField(blank=True)
    contenido = models.TextField()
    imagen_destacada = models.ImageField(upload_to="blog/", blank=True, null=True)
    categoria = models.ForeignKey(CategoriaBlog, on_delete=models.SET_NULL, null=True, blank=True, related_name="posts")
    etiquetas = models.ManyToManyField(EtiquetaBlog, blank=True, related_name="posts")
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="posts_blog")
    # Nombre público del escritor; el usuario que creó el registro se conserva en `autor`.
    autor_nombre = models.CharField(max_length=150, blank=True)
    estado = models.CharField(max_length=10, choices=ESTADOS, default="BORRADOR")
    meta_titulo = models.CharField(max_length=200, blank=True)
    meta_descripcion = models.CharField(max_length=300, blank=True)
    fecha_publicacion = models.DateTimeField(blank=True, null=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-fecha_publicacion", "-creado_en"]
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        indexes = [
            models.Index(fields=["estado", "-fecha_publicacion"]),
            models.Index(fields=["slug"]),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
        if self.estado == "PUBLICADO" and self.fecha_publicacion is None:
            self.fecha_publicacion = timezone.now()

        # Normaliza automáticamente la imagen destacada para que todas las
        # tarjetas y portadas del blog tengan el mismo formato.
        if self.imagen_destacada and getattr(self.imagen_destacada, "file", None):
            try:
                self.imagen_destacada.file.seek(0)
                imagen = Image.open(self.imagen_destacada.file)
                imagen = ImageOps.exif_transpose(imagen)

                # Formato panorámico 3:2, adecuado para index, listado y artículo.
                ancho, alto = 1200, 800
                origen_ratio = imagen.width / imagen.height
                destino_ratio = ancho / alto

                if origen_ratio > destino_ratio:
                    nuevo_ancho = int(imagen.height * destino_ratio)
                    izquierda = (imagen.width - nuevo_ancho) // 2
                    imagen = imagen.crop((izquierda, 0, izquierda + nuevo_ancho, imagen.height))
                elif origen_ratio < destino_ratio:
                    nuevo_alto = int(imagen.width / destino_ratio)
                    arriba = (imagen.height - nuevo_alto) // 2
                    imagen = imagen.crop((0, arriba, imagen.width, arriba + nuevo_alto))

                imagen = imagen.resize((ancho, alto), Image.Resampling.LANCZOS)

                if imagen.mode not in ("RGB", "L"):
                    fondo = Image.new("RGB", imagen.size, "white")
                    if "A" in imagen.getbands():
                        fondo.paste(imagen, mask=imagen.getchannel("A"))
                    else:
                        fondo.paste(imagen)
                    imagen = fondo
                else:
                    imagen = imagen.convert("RGB")

                buffer = BytesIO()
                imagen.save(buffer, format="JPEG", quality=86, optimize=True, progressive=True)
                nombre = f"{slugify(self.titulo) or 'post'}.jpg"
                self.imagen_destacada.save(nombre, ContentFile(buffer.getvalue()), save=False)
            except (OSError, ValueError):
                # Si el archivo no es una imagen válida, Django conserva el
                # archivo original y la validación del formulario se encarga.
                pass

        super().save(*args, **kwargs)

    @property
    def publicado(self):
        return self.estado == "PUBLICADO"

    def __str__(self):
        return self.titulo


class InteraccionWeb(models.Model):
    TIPOS = [("CONTACTO", "Contacto"), ("AGENDAMIENTO", "Solicitud de agendamiento")]
    ESTADOS = [("PENDIENTE", "Pendiente"), ("CONTACTADO", "Contactado"), ("CONFIRMADO", "Confirmado"), ("NO_CONCRETADO", "No concretado")]
    tipo = models.CharField(max_length=20, choices=TIPOS)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    email = models.EmailField()
    telefono = models.CharField(max_length=30)
    servicio = models.CharField(max_length=150, blank=True)
    fecha_solicitada = models.DateField(null=True, blank=True)
    mensaje = models.TextField(blank=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default="PENDIENTE")
    observaciones = models.TextField(blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-creado_en"]
        verbose_name = "Interacción web"
        verbose_name_plural = "Interacciones web"

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.nombres} {self.apellidos}"


class InteraccionWebHistorial(models.Model):
    interaccion = models.ForeignKey(InteraccionWeb, on_delete=models.CASCADE, related_name="historial")
    estado_anterior = models.CharField(max_length=20)
    estado_nuevo = models.CharField(max_length=20)
    comentario = models.TextField(blank=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-creado_en"]
        verbose_name = "Historial de interacción web"
        verbose_name_plural = "Historial de interacciones web"
