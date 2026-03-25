from django.urls import path
from .views import ( DetalleQuejaView, ListaQuejasView, RegistroView, PerfilView, BuzonQuejasView, ListaUsuariosView)

urlpatterns = [
    path('registro/', RegistroView.as_view()),
    path('perfil/', PerfilView.as_view()),
    path('buzon-quejas/', BuzonQuejasView.as_view()),
    path('lista/', ListaUsuariosView.as_view()),
    path('quejas/', ListaQuejasView.as_view()),
    path('quejas/<uuid:uuid>/', DetalleQuejaView.as_view()),
]