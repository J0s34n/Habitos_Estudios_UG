# 📚 Habitos de Estudios

Sistema web para identificar y mejorar los hábitos de estudio de estudiantes universitarios, mediante evaluaciones personalizadas y recomendaciones generadas con Machine Learning.

---

## 🛠 Stack Tecnológico

| Capa | Tecnología |
|------|-----------|
| Frontend | Vue 3 + Vite + Tailwind CSS |
| Backend | Django 4.2 + Django REST Framework |
| Autenticación | JWT (SimpleJWT) |
| Base de datos | SQLite (desarrollo) |
| Machine Learning | scikit-learn (KNN) |
| PDF | jsPDF + jspdf-autotable |

---

## 📋 Requisitos Previos

- Python 3.10+
- Node.js 18+
- Git

---

## 🚀 Instalación y Configuración

### 1. Clonar el repositorio

```cmd
git clone https://github.com/J0s34n/Habitos_Estudios_UG.git
cd Habitos_Estudios_UG
git checkout desarrollo
```

### 2. Configurar el Backend (Django)

```cmd
# Crear y activar entorno virtual
python -m venv venv

# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 3. Configurar la base de datos

```cmd
# Crear migraciones
python manage.py makemigrations usuarios tests_app resultados reportes

# Aplicar migraciones
python manage.py migrate

# Crear superusuario administrador
python manage.py createsuperuser

# Cargar preguntas iniciales del test
python manage.py loaddata apps/tests_app/fixtures/test_inicial.json

# Entrenar modelo ML
python manage.py shell -c "from apps.ml_engine.predictor import entrenar_modelo; entrenar_modelo()"
```

### 4. Configurar el Frontend (Vue)

```cmd
cd frontend
npm install
```

---

## ▶️ Ejecutar el Proyecto

Necesitas **dos terminales** abiertas simultáneamente:

**Terminal 1 — Backend:**
```cmd
# Activa el entorno virtual si no está activo
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

python manage.py runserver
```
Backend disponible en: `http://localhost:8000`

**Terminal 2 — Frontend:**
```cmd
cd frontend
npm run dev
```
App disponible en: `http://localhost:5173`

---

## 👥 Roles de Usuario

| Rol | Acceso |
|-----|--------|
| **Estudiante** | Realizar tests, ver resultados, evaluaciones pasadas, perfil, buzón |
| **Administrador** | Dashboard, gestión de tests, estudiantes, respuestas, reportes, quejas |

### Crear un administrador adicional

```cmd
python manage.py shell
```
```python
from apps.usuarios.models import Usuario

u = Usuario.objects.create_user(
    username='admin2',
    email='admin2@ejemplo.com',
    password='password123',
    first_name='Admin',
    rol='admin'
)
u.is_staff = True
u.save()
print("✅ Administrador creado")
```

---

## 🧠 Machine Learning

El sistema usa dos capas de análisis:

1. **Reglas por score** — Clasifica cada área (tiempo, métodos, entorno) en nivel alto/medio/bajo y genera recomendaciones específicas. Funciona desde el primer uso sin datos históricos.

2. **Clasificador KNN** — Predice el perfil del estudiante entre 5 categorías. Entrenado inicialmente con datos sintéticos, mejora con datos reales acumulados.

### Áreas evaluadas

| Área | Descripción |
|------|-------------|
| ⏱ Gestión del Tiempo | Organización, planificación y cumplimiento de horarios |
| 📚 Métodos de Estudio | Técnicas, toma de apuntes y repaso del contenido |
| 🏠 Entorno Personal | Espacio de estudio, distracciones y motivación |

### Reentrenar el modelo con datos reales

```bash
python manage.py shell
```
```python
from apps.resultados.models import Resultado
from apps.ml_engine.predictor import entrenar_modelo
import numpy as np

datos = Resultado.objects.values_list('score_tiempo', 'score_metodos', 'score_entorno')
print(f"Datos disponibles: {len(datos)}")
# Con suficientes datos, adaptar entrenar_modelo() para usar datos reales
```

---

## 📁 Estructura del Proyecto

```
Habitos_Estudios_UG/
├── apps/
│   ├── usuarios/        # Modelo de usuario, registro, perfil, buzón
│   ├── tests_app/       # Tests, preguntas y opciones
│   ├── resultados/      # Respuestas y resultados de tests
│   ├── reportes/        # Generación y descarga de reportes
│   └── ml_engine/       # Motor de recomendaciones ML
├── config/
│   ├── settings.py
│   └── urls.py
├── frontend/
│   ├── src/
│   │   ├── views/       # Vistas Vue
│   │   ├── components/  # NavBar, PageContainer
│   │   ├── stores/      # Pinia (auth)
│   │   ├── api/         # Axios configurado
│   │   └── router/      # Vue Router
│   └── package.json
├── requirements.txt
└── manage.py
```

---

## 🔌 API Endpoints Principales

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/auth/login/` | Iniciar sesión |
| POST | `/api/usuarios/registro/` | Registrar usuario |
| GET | `/api/usuarios/perfil/` | Ver/editar perfil |
| GET | `/api/tests/` | Listar tests activos |
| POST | `/api/resultados/enviar/` | Enviar respuestas del test |
| GET | `/api/resultados/mis-resultados/` | Historial del estudiante |
| GET | `/api/reportes/` | Listar reportes (admin) |
| POST | `/api/reportes/generar/` | Generar nuevo reporte (admin) |

---

## ⚙️ Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto:

```env
SECRET_KEY=tu-clave-secreta-aqui
DEBUG=True
```

---

## 🚀 Consideraciones para Producción

Antes de desplegar en producción:

- [ ] Cambiar `DEBUG = False` en `settings.py`
- [ ] Configurar `ALLOWED_HOSTS` con el dominio real
- [ ] Cambiar `CORS_ALLOW_ALL_ORIGINS = False` y especificar dominios
- [ ] Migrar de SQLite a PostgreSQL
- [ ] Configurar variables de entorno seguras
- [ ] Servir frontend con Nginx o similar
- [ ] Implementar UUID en resultados para ocultar IDs

---

## 📌 Versiones Futuras

- Reportes personalizables por rango de fechas y filtros
- Más tipos de test y áreas de evaluación
- Dashboard con más métricas y gráficas

---

## 👨‍💻 Desarrollo

Proyecto desarrollado como sistema de apoyo académico para estudiantes universitarios.

> **Rama principal de desarrollo:** `desarrollo`
