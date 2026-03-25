from rest_framework.views import APIView
from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import Reporte
from .serializers import ReporteSerializer
from apps.resultados.models import Resultado
from apps.usuarios.models import Usuario
from apps.tests_app.models import Test
from django.db.models import Avg

class ListaReportesView(generics.ListAPIView):
    serializer_class = ReporteSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = Reporte.objects.all()

class GenerarReporteView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        tipo = request.data.get('tipo')
        if tipo not in ['general', 'comparativa', 'criticas']:
            return Response({'error': 'Tipo inválido'}, status=400)

        datos = self._calcular_datos(tipo)

        reporte = Reporte.objects.create(
            tipo=tipo,
            generado_por=request.user,
            datos=datos
        )

        return Response(ReporteSerializer(reporte).data, status=201)

    def _calcular_datos(self, tipo):
        resultados = Resultado.objects.all()

        if tipo == 'general':
            return {
                'total_respuestas': resultados.count(),
                'total_estudiantes': Usuario.objects.filter(rol='estudiante', is_superuser=False, is_staff=False).count(),
                'total_tests': Test.objects.filter(activo=True).count(),
                'promedio_tiempo': round(
                    resultados.aggregate(p=Avg('score_tiempo'))['p'] or 0, 1),
                'promedio_metodos': round(
                    resultados.aggregate(p=Avg('score_metodos'))['p'] or 0, 1),
                'promedio_entorno': round(
                    resultados.aggregate(p=Avg('score_entorno'))['p'] or 0, 1),
            }

        elif tipo == 'comparativa':
            tests = Test.objects.all()
            comparativa = []
            for test in tests:
                qs = resultados.filter(test=test)
                if qs.exists():
                    comparativa.append({
                        'test_nombre': test.nombre,
                        'promedio_tiempo': round(
                            qs.aggregate(p=Avg('score_tiempo'))['p'] or 0, 1),
                        'promedio_metodos': round(
                            qs.aggregate(p=Avg('score_metodos'))['p'] or 0, 1),
                        'promedio_entorno': round(
                            qs.aggregate(p=Avg('score_entorno'))['p'] or 0, 1),
                        'total_respuestas': qs.count(),
                    })
            return {'tests': comparativa}

        elif tipo == 'criticas':
            promedio_tiempo = round(
                resultados.aggregate(p=Avg('score_tiempo'))['p'] or 0, 1)
            promedio_metodos = round(
                resultados.aggregate(p=Avg('score_metodos'))['p'] or 0, 1)
            promedio_entorno = round(
                resultados.aggregate(p=Avg('score_entorno'))['p'] or 0, 1)

            areas = [
                ('Gestión del Tiempo', promedio_tiempo),
                ('Métodos de Estudio', promedio_metodos),
                ('Entorno Personal', promedio_entorno),
            ]
            areas_ordenadas = sorted(areas, key=lambda x: x[1], reverse=True)

            return {
                'promedio_tiempo': promedio_tiempo,
                'promedio_metodos': promedio_metodos,
                'promedio_entorno': promedio_entorno,
                'area_critica': areas_ordenadas[0][0],
                'total_analizados': resultados.count(),
            }

        return {}

class EliminarReporteView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = Reporte.objects.all()
    lookup_field = 'uuid'