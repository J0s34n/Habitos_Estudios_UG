from django.urls import path
from .views import (ListaTestsView, DetalleTestView, CrearTestView,
                    EditarTestView, ToggleTestView,
                    AgregarPreguntaView, EditarPreguntaView)

urlpatterns = [
    path('', ListaTestsView.as_view()),
    path('<int:pk>/', DetalleTestView.as_view()),
    path('crear/', CrearTestView.as_view()),
    path('<int:pk>/editar/', EditarTestView.as_view()),
    path('<int:pk>/toggle/', ToggleTestView.as_view()),
    path('preguntas/agregar/', AgregarPreguntaView.as_view()),
    path('preguntas/<int:pk>/', EditarPreguntaView.as_view()),
]