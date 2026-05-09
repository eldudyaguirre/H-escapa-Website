from django.urls import path, include
from . import views
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views
from django.contrib.sitemaps.views import sitemap
from store.sitemaps import StaticViewSitemap

sitemaps = {
    'static': StaticViewSitemap,
}

urlpatterns = [
    path('', views.home, name='home'),
    path('inicio/', views.homein, name='homein'),

    path('about/', views.about, name='about'),
    path('contact/', views.contactanos, name='contact'),
    path('agendamiento/', views.agendamiento, name='agendamiento'),

    path('services/', views.services, name='services'),
    path('individualtherapy/', views.individualtherapy, name='individualtherapy'),
    path('coupletherapy/', views.coupletherapy, name='coupletherapy'),
    path('grupaltherapy/', views.grupaltherapy, name='grupaltherapy'),
    path('kidstherapy/', views.kidstherapy, name='kidstherapy'),
    path('depansitherapy/', views.depansitherapy, name='depansitherapy'),
    path('judgeservices/', views.judgeservices, name='judgeservices'),
    path('meditation/', views.meditation, name='meditation'),
    path('blog-general/', views.bloggeneral, name='bloggeneral'),
    path('blog-detalle/', views.blogdetalle, name='blogdetalle'),

    path('ayuda-sos/', views.ayudasos, name='ayudasos'),
    path('guerrero-valiente/', views.guerrerovaliente, name='guerrerovaliente'),
    path('kchetazo-mental/', views.kchetazomental, name='kchetazomental'),
    path('team-hp/', views.teamhp, name='teamhp'),

    path('signin/', views.signin, name='signin'),
    path('logout/', views.do_logout, name='logout'),
    path('homein/', views.homein, name='homein'),   

    path('homein-calendario/', views.homeincalendario, name='homeincalendario'),   
    path('homein-nuevopaciente/', views.homeinnuevopaciente, name='homeinnuevopaciente'),   
    path(
        'sitemap.xml',
        sitemap,
        {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'
    ),
]



