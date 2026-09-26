from django.contrib import admin

from .models import (
    CategoriaBlog,
    Cita,
    EtiquetaBlog,
    HistoriaClinica,
    Paciente,
    Post,
    Profesional,
)


admin.site.site_header = "Página Web de Hester Palacio H-Escapa"
admin.site.site_title = "H-Escapa"
admin.site.index_title = "Administración"


@admin.register(Profesional)
class ProfesionalAdmin(admin.ModelAdmin):
    list_display = ("nombre", "apellido", "especialidad", "activo")
    list_filter = ("especialidad", "activo")
    search_fields = ("nombre", "apellido", "usuario__username", "usuario__email")


@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ("nombres", "apellidos", "correo", "telefono", "profesional", "estado")
    list_filter = ("estado", "genero", "tipo_sangre")
    search_fields = ("nombres", "apellidos", "correo", "telefono")
    list_select_related = ("profesional",)


@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ("fecha_hora", "paciente", "profesional", "modalidad", "estado")
    list_filter = ("estado", "modalidad", "profesional")
    search_fields = (
        "paciente__nombres",
        "paciente__apellidos",
        "profesional__nombre",
        "profesional__apellido",
    )
    date_hierarchy = "fecha_hora"
    list_select_related = ("paciente", "profesional")


@admin.register(HistoriaClinica)
class HistoriaClinicaAdmin(admin.ModelAdmin):
    list_display = ("fecha", "paciente", "profesional", "cita")
    list_filter = ("profesional",)
    search_fields = (
        "paciente__nombres",
        "paciente__apellidos",
        "diagnostico",
        "motivo_consulta",
    )
    date_hierarchy = "fecha"
    list_select_related = ("paciente", "profesional", "cita")


@admin.register(CategoriaBlog)
class CategoriaBlogAdmin(admin.ModelAdmin):
    list_display = ("nombre", "slug", "activa")
    list_filter = ("activa",)
    search_fields = ("nombre",)
    prepopulated_fields = {"slug": ("nombre",)}


@admin.register(EtiquetaBlog)
class EtiquetaBlogAdmin(admin.ModelAdmin):
    list_display = ("nombre", "slug")
    search_fields = ("nombre",)
    prepopulated_fields = {"slug": ("nombre",)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "titulo",
        "categoria",
        "autor",
        "estado",
        "fecha_publicacion",
        "actualizado_en",
    )
    list_filter = ("estado", "categoria")
    search_fields = ("titulo", "resumen", "contenido", "meta_titulo", "meta_descripcion")
    prepopulated_fields = {"slug": ("titulo",)}
    filter_horizontal = ("etiquetas",)
    date_hierarchy = "fecha_publicacion"
    list_select_related = ("categoria", "autor")
