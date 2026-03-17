from django.urls import path
from .views import EnviarRespuestasView, MisResultadosView, DetalleResultadoView ,TodosResultadosView

urlpatterns = [
    path('enviar/', EnviarRespuestasView.as_view()),
    path('mis-resultados/', MisResultadosView.as_view()),
    path('mis-resultados/<uuid:uuid>/', DetalleResultadoView.as_view()),
    path('todos/', TodosResultadosView.as_view()),
]
