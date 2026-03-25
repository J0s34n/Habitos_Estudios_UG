from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegistroSerializer, UsuarioSerializer, QuejaSerializer
from django.contrib.auth import get_user_model
from .models import Queja

Usuario = get_user_model()

class RegistroView(generics.CreateAPIView):
    serializer_class = RegistroSerializer
    permission_classes = [permissions.AllowAny]

class PerfilView(generics.RetrieveUpdateAPIView):
    serializer_class = UsuarioSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        if instance.is_superuser or instance.is_staff or instance.rol == 'admin':
            data['rol'] = 'admin'
        return Response(data)

class BuzonQuejasView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        tipo = request.data.get('tipo') #queja o sugerencia
        comentario = request.data.get('comentario')
        email = request.data.get('email')
        if not all([tipo, comentario, email]):
            return Response({'error': 'Todos los campos son requeridos'}, status=status.HTTP_400_BAD_REQUEST)
        Queja.objects.create(tipo=tipo, comentario=comentario, email=email)
        return Response({'message': 'Gracias por tu feedback'}, status=status.HTTP_201_CREATED)
    
class ListaUsuariosView(generics.ListAPIView):
    serializer_class = UsuarioSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = Usuario.objects.filter(rol='estudiante', is_staff=False, is_superuser=False)  

class ListaQuejasView(generics.ListAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = Queja.objects.all()
    serializer_class = QuejaSerializer

class DetalleQuejaView(generics.RetrieveDestroyAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = Queja.objects.all()
    serializer_class = QuejaSerializer
    lookup_field = 'uuid'