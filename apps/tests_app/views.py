from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Test, Pregunta, Opcion
from .serializers import TestSerializer, PreguntaSerializer, CrearTestSerializer

class ListaTestsView(generics.ListAPIView):
    serializer_class = TestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.rol == 'admin':
            return Test.objects.all()
        return Test.objects.filter(activo=True)

class DetalleTestView(generics.RetrieveAPIView):
    serializer_class = TestSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Test.objects.all()

class CrearTestView(generics.CreateAPIView):
    serializer_class = CrearTestSerializer
    permission_classes = [permissions.IsAdminUser]

class EditarTestView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CrearTestSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = Test.objects.all()

class ToggleTestView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def patch(self, request, pk):
        test = Test.objects.get(pk=pk)
        test.activo = not test.activo
        test.save()
        return Response({'activo': test.activo})

class AgregarPreguntaView(generics.CreateAPIView):
    serializer_class = PreguntaSerializer
    permission_classes = [permissions.IsAdminUser]

class EditarPreguntaView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PreguntaSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = Pregunta.objects.all()