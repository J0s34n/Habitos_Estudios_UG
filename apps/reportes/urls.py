from django.urls import path
from .views import *

urlpatterns = [
    path('', ListaReportesView.as_view(), name='lista_reportes'),
    path('generar/', GenerarReporteView.as_view(), name='generar_reporte'),
    path('<int:pk>/', EliminarReporteView.as_view(), name='detalle_reporte'),    
    ]

