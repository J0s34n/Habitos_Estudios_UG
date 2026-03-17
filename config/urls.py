from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from apps.usuarios.serializers import CustomTokenSerializer

class CustomTokenView(TokenObtainPairView):
    serializer_class = CustomTokenSerializer

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/login/', CustomTokenView.as_view(), name='token_obtain'),  # ← CustomTokenView no TokenObtainPairView
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/usuarios/', include('apps.usuarios.urls')),
    path('api/tests/', include('apps.tests_app.urls')),
    path('api/resultados/', include('apps.resultados.urls')),
    path('api/reportes/', include('apps.reportes.urls')),
]