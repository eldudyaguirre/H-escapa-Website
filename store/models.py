from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class Profesional(models.Model):
    ESPECIALIDADES = [
        ("PSICOLOGIA", "Psicología"),
        ("PSICOLOGIA_CLINICA", "Psicología Clínica"),
        ("TERAPIA_FAMILIAR", "Terapia Familiar"),
        ("TERAPIA_PAREJA", "Terapia de Pareja"),
        ("OTRA", "Otra"),
    ]

    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profesional",
    )
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    especialidad = models.CharField(
        max_length=30,
        choices=ESPECIALIDADES,
        default="PSICOLOGIA_CLINICA",
    )
    telefono = models.CharField(max_length=30, blank=True)
    activo = models.BooleanField(default=True)
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

    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    genero = models.CharField(max_length=1, choices=GENEROS, blank=True)
    correo = models.EmailField(blank=True)
    telefono = models.CharField(max_length=30, blank=True)
    direccion = models.CharField(max_length=250, blank=True)
    tipo_sangre = models.CharField(
        max_length=3,
        choices=TIPOS_SANGRE,
        default="ND",
    )
    contacto_emergencia = models.CharField(max_length=150, blank=True)
    telefono_emergencia = models.CharField(max_length=30, blank=True)
    profesional = models.ForeignKey(
        Profesional,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="pacientes",
    )
    estado = models.CharField(
        max_length=10,
        choices=ESTADOS,
        default="ACTIVO",
    )
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

    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.PROTECT,
        related_name="citas",
    )
    profesional = models.ForeignKey(
        Profesional,
        on_delete=models.PROTECT,
        related_name="citas",
    )
    fecha_hora = models.DateTimeField()
    duracion_minutos = models.PositiveIntegerField(default=60)
    modalidad = models.CharField(
        max_length=12,
        choices=MODALIDADES,
        default="PRESENCIAL",
    )
    estado = models.CharField(
        max_length=12,
        choices=ESTADOS,
        default="PROGRAMADA",
    )
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
    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        related_name="historias_clinicas",
    )
    profesional = models.ForeignKey(
        Profesional,
        on_delete=models.PROTECT,
        related_name="historias_clinicas",
    )
    cita = models.ForeignKey(
        Cita,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="registros_clinicos",
    )
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
    imagen_destacada = models.ImageField(
        upload_to="blog/",
        blank=True,
        null=True,
    )
    categoria = models.ForeignKey(
        CategoriaBlog,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="posts",
    )
    etiquetas = models.ManyToManyField(
        EtiquetaBlog,
        blank=True,
        related_name="posts",
    )
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="posts_blog",
    )
    estado = models.CharField(
        max_length=10,
        choices=ESTADOS,
        default="BORRADOR",
    )
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

        super().save(*args, **kwargs)

    @property
    def publicado(self):
        return self.estado == "PUBLICADO"

    def __str__(self):
        return self.titulo
