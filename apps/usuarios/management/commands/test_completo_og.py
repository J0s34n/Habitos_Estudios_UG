from apps.tests_app.models import Test, Pregunta, Opcion

test = Test.objects.get(id=1)  # ajusta el id si es diferente

preguntas = [
  # ── ÁREA: TIEMPO ──────────────────────────────────────────
    {
    'texto': '¿Cuándo empiezas a estudiar para un examen?',
    'area': 'tiempo', 'orden': 2,
    'opciones': [
      ('Con varios días o semanas de anticipación.', 'A', 1),
      ('Unos días antes del examen.', 'B', 2),
      ('Un día antes.', 'C', 3),
      ('El mismo día o pocas horas antes.', 'D', 4),
    ]
  },
  {
    'texto': '¿Cuánto tiempo dedicas al estudio fuera de clases?',
    'area': 'tiempo', 'orden': 3,
    'opciones': [
      ('Estudio diariamente según mi planificación.', 'A', 1),
      ('Estudio varias veces por semana.', 'B', 2),
      ('Solo cuando hay tareas o exámenes.', 'C', 3),
      ('Casi nunca estudio fuera de clase.', 'D', 4),
    ]
  },
  {
    'texto': '¿Qué tan bien cumples con las fechas de entrega?',
    'area': 'tiempo', 'orden': 4,
    'opciones': [
      ('Siempre entrego antes o en la fecha.', 'A', 1),
      ('Casi siempre entrego a tiempo.', 'B', 2),
      ('A veces entrego tarde.', 'C', 3),
      ('Frecuentemente entrego tarde o no entrego.', 'D', 4),
    ]
  },
  {
    'texto': '¿Qué haces cuando tienes muchas tareas?',
    'area': 'tiempo', 'orden': 5,
    'opciones': [
      ('Las priorizo y hago un plan.', 'A', 1),
      ('Intento avanzar en varias a la vez.', 'B', 2),
      ('Empiezo por la más fácil.', 'C', 3),
      ('Me siento abrumado y lo dejo para después.', 'D', 4),
    ]
  },
  # ── ÁREA: MÉTODOS ─────────────────────────────────────────
  {
    'texto': '¿Cómo estudias normalmente?',
    'area': 'metodos', 'orden': 6,
    'opciones': [
      ('Uso técnicas como resúmenes, mapas conceptuales o ejercicios.', 'A', 1),
      ('Leo y subrayo el contenido.', 'B', 2),
      ('Solo leo el material varias veces.', 'C', 3),
      ('Repaso rápido sin una técnica clara.', 'D', 4),
    ]
  },
  {
    'texto': '¿Qué haces cuando no entiendes un tema?',
    'area': 'metodos', 'orden': 7,
    'opciones': [
      ('Busco información adicional o pido ayuda.', 'A', 1),
      ('Reviso el material nuevamente.', 'B', 2),
      ('Lo dejo para después.', 'C', 3),
      ('Lo ignoro y sigo adelante.', 'D', 4),
    ]
  },
  {
    'texto': '¿Cómo tomas apuntes en clase?',
    'area': 'metodos', 'orden': 8,
    'opciones': [
      ('Tomo apuntes organizados y completos.', 'A', 1),
      ('Tomo apuntes básicos.', 'B', 2),
      ('Tomo pocos apuntes.', 'C', 3),
      ('No tomo apuntes.', 'D', 4),
    ]
  },
  {
    'texto': '¿Cómo repasas lo aprendido?',
    'area': 'metodos', 'orden': 9,
    'opciones': [
      ('Repaso regularmente lo visto en clase.', 'A', 1),
      ('Repaso antes de las evaluaciones.', 'B', 2),
      ('Solo reviso lo más importante.', 'C', 3),
      ('No repaso el contenido.', 'D', 4),
    ]
  },
  {
    'texto': '¿Qué haces para recordar mejor la información?',
    'area': 'metodos', 'orden': 10,
    'opciones': [
      ('Practico ejercicios o explico el tema.', 'A', 1),
      ('Hago resúmenes o esquemas.', 'B', 2),
      ('Leo varias veces.', 'C', 3),
      ('Confío solo en mi memoria.', 'D', 4),
    ]
  },
  # ── ÁREA: ENTORNO ─────────────────────────────────────────
  {
    'texto': '¿Dónde sueles estudiar?',
    'area': 'entorno', 'orden': 11,
    'opciones': [
      ('En un lugar tranquilo y sin distracciones.', 'A', 1),
      ('En un lugar relativamente tranquilo.', 'B', 2),
      ('En lugares con algunas distracciones.', 'C', 3),
      ('En lugares muy distractores (TV, celular, ruido).', 'D', 4),
    ]
  },
  {
    'texto': '¿Qué tan fácil te distraes al estudiar?',
    'area': 'entorno', 'orden': 12,
    'opciones': [
      ('Mantengo la concentración la mayor parte del tiempo.', 'A', 1),
      ('Me distraigo ocasionalmente.', 'B', 2),
      ('Me distraigo con frecuencia.', 'C', 3),
      ('Me distraigo casi siempre.', 'D', 4),
    ]
  },
  {
    'texto': '¿Qué papel juega el celular o redes sociales al estudiar?',
    'area': 'entorno', 'orden': 13,
    'opciones': [
      ('Lo mantengo lejos o en silencio.', 'A', 1),
      ('Lo reviso ocasionalmente.', 'B', 2),
      ('Lo reviso con frecuencia.', 'C', 3),
      ('Lo uso constantemente mientras estudio.', 'D', 4),
    ]
  },
  {
    'texto': '¿Cómo te sientes respecto al estudio?',
    'area': 'entorno', 'orden': 14,
    'opciones': [
      ('Motivado y comprometido con aprender.', 'A', 1),
      ('A veces motivado.', 'B', 2),
      ('Poco motivado.', 'C', 3),
      ('Desmotivado o sin interés.', 'D', 4),
    ]
  },
  {
    'texto': '¿Qué haces cuando un tema es difícil?',
    'area': 'entorno', 'orden': 15,
    'opciones': [
      ('Persisto hasta entenderlo.', 'A', 1),
      ('Lo intento un tiempo.', 'B', 2),
      ('Lo dejo para después.', 'C', 3),
      ('Lo abandono.', 'D', 4),
    ]
  },
]

# Insertar todo
for p_data in preguntas:
    opciones = p_data.pop('opciones')
    p = Pregunta.objects.create(test=test, **p_data)
    for texto, letra, peso in opciones:
        Opcion.objects.create(pregunta=p, texto=texto, letra=letra, peso=peso)

print(f"✅ {Pregunta.objects.filter(test=test).count()} preguntas en el test")