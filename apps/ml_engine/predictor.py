""""
Motor de ML para recomendaciones de habitos de estudio basado en scores de tiempo, métodos y entorno. Utiliza un modelo simple para generar recomendaciones personalizadas según el área más débil del usuario. Integrado con el sistema de resultados para ofrecer feedback inmediato.
Usa un clasificador KNN entrenado con datos históricos de usuarios para predecir recomendaciones basadas en los scores obtenidos en las áreas de tiempo, métodos y entorno. El modelo se actualiza periódicamente con nuevos resultados para mejorar su precisión.
En produccion: Reemplazar con datos reales de la BD
"""

import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
import joblib
import os

#Base de conocimiento: Recomendacion por area y severidad
RECOMENDACIONES = {
    'tiempo': {
        'alta': [
            "Implementa la técnica Pomodoro: 25 min de estudio, 5 de descanso.",
            "Usa un planificador semanal y agenda bloques de estudio fijos.",
            "Identifica tus 'ladrones de tiempo' y elimínalos de tu rutina.",
            "Establece metas diarias específicas y medibles antes de estudiar.",
        ],
        'media': [
            "Prueba crear un horario de estudio con al menos 3 días fijos por semana.",
            "Usa apps como Google Calendar para recordatorios de sesiones de estudio.",
        ],
        'baja': [
            "¡Vas bien con el tiempo! Considera revisar y optimizar tu horario mensualmente.",
        ]
    },
    'metodos': {
        'alta': [
            "Estudia en un lugar libre de distracciones, sin celular visible.",
            "Aprende y practica el método Cornell para tomar apuntes efectivos.",
            "Evita el multitasking: enfócate en una sola materia por sesión.",
            "Usa mapas mentales para organizar y repasar el contenido.",
        ],
        'media': [
            "Experimenta con diferentes técnicas: flashcards, resúmenes, mapas conceptuales.",
            "Repasa el material estudiado dentro de las 24 horas siguientes.",
        ],
        'baja': [
            "Tus métodos de estudio son sólidos. Comparte tus técnicas con compañeros.",
        ]
    },
    'entorno': {
        'alta': [
            "Crea un espacio de estudio dedicado, limpio, bien iluminado y silencioso.",
            "Establece una rutina pre-estudio (música instrumental, té, revisar agenda).",
            "Trabaja en tu motivación: escribe por qué es importante alcanzar tus metas.",
            "Busca un grupo de estudio para mantener la disciplina y responsabilidad.",
        ],
        'media': [
            "Personaliza tu espacio de estudio para hacerlo más cómodo y estimulante.",
            "Practica técnicas de mindfulness de 5 minutos antes de estudiar.",
        ],
        'baja': [
            "Tu entorno y actitud son positivos. Mantén esa mentalidad de crecimiento.",
        ]
    }
}

def generar_recomendaciones(score_tiempo: float, score_metodos: float, score_entorno: float) -> list:
    """"
    Generar recomendaciones personalizadas basadas en los scores de debilidad.
    Score: 0-100, donde mayor es debil en esa area
    """
    recomendaciones = []

    areas = {
        'tiempo': score_tiempo,
        'metodos': score_metodos,
        'entorno': score_entorno
    }

    # Ordenar areas de mayor a menor debilidad
    areas_ordenadas = sorted(areas.items(), key=lambda x: x[1], reverse=True)
    for area, score in areas_ordenadas:
        if score >= 65:
          nivel = 'alta'
          # Tomar 3 recomendaciones prioritarias
          recs = RECOMENDACIONES[area][nivel][:3]
        elif score >= 40:
            nivel = 'media'
            recs = RECOMENDACIONES[area][nivel][:2]
        else:
            nivel = 'baja'
            recs = RECOMENDACIONES[area][nivel][:1]
        
        for rec in recs:
            recomendaciones.append({'area': area, 'nivel': nivel, 'texto': rec})
    return recomendaciones

#--- Modelo ML (KNN) para clasificaficacion del perfil ---#

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'modelo_habitos.joblib')
SCALER_PATH = os.path.join(os.path.dirname(__file__), 'scaler.joblib')

PERFILES = {
    0: 'Estudiante Organizado',
    1: 'Estudiante con Dificultad de Tiempo',
    2: 'Estudiante con Dificultad de Métodos',
    3: 'Estudiante con Dificultad de Entorno',
    4: 'Estudiante con Múltiples Dificultades',
}

def entrenar_modelo():
    """
    Entrenar un modelo KNN con datos sinteticos representativos
    En produccion, reemplazar con datos reales de la BD
    """
    # Datos de entrenamiento sintéticos [score_tiempo, score_metodos, score_entorno] -> perfil
    X_train = np.array([
        [20, 15, 10], [25, 20, 15], [15, 25, 20], # Organizado
        [80, 20, 20], [75, 15, 25], [85, 30, 15], # Dificultad de Tiempo
        [20, 80, 20], [25, 75, 15], [15, 85, 25], # Dificultad de Métodos
        [20, 20, 80], [15, 25, 75], [25, 15, 85], # Dificultad de Entorno
        [70, 65, 70], [75, 70, 65], [65, 75, 70], # Múltiples Dificultades
    ])
    y = np.array([0,0,0, 1,1,1, 2,2,2, 3,3,3, 4,4,4])

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_train)

    knn = KNeighborsClassifier(n_neighbors=3)
    knn.fit(X_scaled, y)

    joblib.dump(knn, MODEL_PATH)
    joblib.dump(scaler, SCALER_PATH)
    print("Modelo entrenado y guardado.")
    return knn, scaler

def predecir_perfil(score_tiempo, score_metodos, score_entorno) -> str:
    """"
    Predecir el perfil del estudiante basado en los scores usando el modelo KNN
    """
    if not os.path.exists(MODEL_PATH) or not os.path.exists(SCALER_PATH):
        entrenar_modelo()
    
    knn = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)

    X_test = np.array([[score_tiempo, score_metodos, score_entorno]])
    X_test_scaled = scaler.transform(X_test)
    perfil_predicho = knn.predict(X_test_scaled)[0]
    return PERFILES[perfil_predicho]