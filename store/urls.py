from django.contrib.sitemaps.views import sitemap
from django.urls import path
from . import views
from store.sitemaps import StaticViewSitemap

sitemaps = {"static": StaticViewSitemap}

urlpatterns = [
    path("", views.home, name="home"),
    path("inicio/", views.homein, name="homein"),
    path("about/", views.about, name="about"),
    path("contact/", views.contactanos, name="contact"),
    path("agendamiento/", views.agendamiento, name="agendamiento"),
    path("services/", views.services, name="services"),
    path("individualtherapy/", views.individualtherapy, name="individualtherapy"),
    path("coupletherapy/", views.coupletherapy, name="coupletherapy"),
    path("grupaltherapy/", views.grupaltherapy, name="grupaltherapy"),
    path("kidstherapy/", views.kidstherapy, name="kidstherapy"),
    path("depansitherapy/", views.depansitherapy, name="depansitherapy"),
    path("judgeservices/", views.judgeservices, name="judgeservices"),
    path("meditation/", views.meditation, name="meditation"),
    path("blog-general/", views.bloggeneral, name="bloggeneral"),
    path("blog/<slug:slug>/", views.blogdetalle, name="blogdetalle"),
    path("ayuda-sos/", views.ayudasos, name="ayudasos"),
    path("guerrero-valiente/", views.guerrerovaliente, name="guerrerovaliente"),
    path("kchetazo-mental/", views.kchetazomental, name="kchetazomental"),
    path("team-hp/", views.teamhp, name="teamhp"),
    path("signin/", views.signin, name="signin"),
    path("logout/", views.do_logout, name="logout"),
    path("homein/", views.homein, name="homein"),
    path("homein-calendario/", views.homeincalendario, name="homeincalendario"),
    path("homein-profesionales/", views.homeinprofesionales, name="homeinprofesionales"),
    path("homein-especialidades/", views.homeinespecialidades, name="homeinespecialidades"),
    path("homein-especialidades/nueva/", views.homeinnuevaespecialidad, name="homeinnuevaespecialidad"),
    path("homein-especialidades/editar/<int:especialidad_id>/", views.homeineditarespecialidad, name="homeineditarespecialidad"),
    path("homein-especialidades/estado/<int:especialidad_id>/", views.cambiar_estado_especialidad, name="cambiar_estado_especialidad"),
    path("homein-pacientes/", views.homeinpacientes, name="homeinpacientes"),
    path("homein-pacientes/foto/<str:paciente_id>/", views.foto_paciente, name="homein_foto_paciente"),
    path("homein-pacientes/perfil/<str:paciente_id>/", views.homeinperfilpaciente, name="homeinperfilpaciente"),
    path("homein-pacientes/perfil/<str:paciente_id>/imprimir/", views.imprimir_perfil_paciente, name="imprimir_perfil_paciente"),
    path("homein-pacientes/editar/<str:paciente_id>/", views.homeineditarpaciente, name="homeineditarpaciente"),
    path("homein-pacientes/estado/<str:paciente_id>/", views.cambiar_estado_paciente, name="cambiar_estado_paciente"),
    path("homein-nuevopaciente/", views.homeinnuevopaciente, name="homeinnuevopaciente"),
    path("homein-nuevacita/", views.homeinnuevacita, name="homeinnuevacita"),
    path(
        "homein-pacientes/<str:paciente_id>/documentos/generar/<str:tipo>/",
        views.generar_documento_paciente,
        name="generar_documento_paciente",
    ),
    path(
        "homein-pacientes/<str:paciente_id>/documentos/subir/",
        views.subir_documento_paciente,
        name="subir_documento_paciente",
    ),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap"),
]
