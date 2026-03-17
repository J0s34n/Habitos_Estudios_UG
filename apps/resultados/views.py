from rest_framework.views import APIView
from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import Resultado, RespuestaDetalle
from .serializers import ResultadoSerializer, EnviarRespuestaSeriallizer
from apps.tests_app.models import Test, Pregunta, Opcion
from apps.ml_engine.predictor import generar_recomendaciones

class EnviarRespuestasView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = EnviarRespuestaSeriallizer(data=request.data)
        if serializer.is_valid():
            test_id = serializer.validated_data['test_id']
            respuestas_raw = serializer.validated_data['respuestas']

            try:
                test = Test.objects.get(id=test_id)
            except Test.DoesNotExist:
                return Response({'error': 'Test no encontrado'}, status=404)

            # Calcular el score y guardar el resultado
            scores = { 'tiempo': [], 'metodos': [], 'entorno': [] }
            for r in respuestas_raw:
                pregunta = Pregunta.objects.get(id=r['pregunta_id'])
                opcion = Opcion.objects.get(id=r['opcion_id'])
                scores[pregunta.area].append(opcion.peso)

            # Normalizar scores con un peso maximo de 4
            def calcular_score(pesos):
                if not pesos:
                    return 0
                return round((sum(pesos) / (len(pesos) * 4)) * 100, 1)
            
            st = calcular_score(scores['tiempo'])
            sm = calcular_score(scores['metodos'])
            se = calcular_score(scores['entorno'])

            area_debil = min([('tiempo', st), ('metodos', sm), ('entorno', se)], key=lambda x: x[1])[0]

            #ML Engine para generar recomendaciones
            recomendaciones = generar_recomendaciones(st, sm, se)

            resultado = Resultado.objects.create(
                usuario=request.user,
                test=test,
                score_tiempo=st,
                score_metodos=sm,
                score_entorno=se,
                area_debil_principal=area_debil,
                recomendaciones=recomendaciones
            )

            # Guardar detalles de respuestas
            for r in respuestas_raw:
                RespuestaDetalle.objects.create(
                    resultado=resultado,
                    pregunta_id=r['pregunta_id'],
                    opcion_seleccionada_id=r['opcion_id']
                )
            return Response(ResultadoSerializer(resultado).data, status=201)
        return Response(serializer.errors, status=400)
    
class MisResultadosView(generics.ListAPIView):
        permission_classes = [permissions.IsAuthenticated]
        serializer_class = ResultadoSerializer

        def get_queryset(self):
            return Resultado.objects.filter(usuario=self.request.user)
        
class TodosResultadosView(generics.ListAPIView):
     permission_classes = [permissions.IsAdminUser]
     serializer_class = ResultadoSerializer
     queryset = Resultado.objects.all()

class DetalleResultadoView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ResultadoSerializer
    lookup_field = 'uuid'

    def get_queryset(self):
        return Resultado.objects.filter(usuario=self.request.user)