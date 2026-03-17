<template>
  <div class="min-h-screen text-white">
    <NavBar />
    <div class="w-full px-4 sm:px-6 lg:px-10 pb-8">

      <!-- ══ Antes de iniciar ══ -->
      <div v-if="!testIniciado">
        <h2 class="text-2xl sm:text-3xl font-black text-center mb-2">ANTES DE INICIAR</h2>
        <h1 class="text-2xl sm:text-4xl font-black text-center mb-8 leading-tight">
          ALGUNAS DE ESTAS ES TU PUNTO DÉBIL
        </h1>

        <!-- Grid: 1 col móvil, 3 col desktop -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 w-full">
          <div v-for="cat in categorias" :key="cat.titulo"
            class="bg-white text-black rounded-2xl p-5">
            <h3 class="font-black text-center mb-4 text-sm leading-tight">{{ cat.titulo }}</h3>
            <ul class="text-xs space-y-2">
              <li v-for="item in cat.items" :key="item" class="flex items-start gap-2">
                <span class="text-blue-600 flex-shrink-0">•</span>
                <span>{{ item }}</span>
              </li>
            </ul>
          </div>
        </div>

        <div class="text-center mt-8">
          <button @click="testIniciado = true"
            class="bg-white text-blue-900 font-bold py-3 px-10 rounded-full
                   hover:bg-blue-100 transition-all">
            INICIAR TEST →
          </button>
        </div>
      </div>

      <!-- ══ Preguntas ══ -->
      <div v-else-if="test && preguntaActual < test.preguntas.length">
        <div class="max-w-2xl mx-auto">
          <!-- Progreso -->
          <div class="mb-3 text-blue-300 text-sm">
            Pregunta {{ preguntaActual + 1 }} de {{ test.preguntas.length }}
          </div>
          <div class="w-full bg-blue-900/40 rounded-full h-2 mb-6">
            <div class="bg-blue-400 h-2 rounded-full transition-all"
              :style="`width: ${((preguntaActual + 1) / test.preguntas.length) * 100}%`" />
          </div>

          <!-- Pregunta -->
          <h2 class="text-lg sm:text-2xl font-black text-center mb-6 uppercase leading-tight">
            {{ pregunta.texto }}
          </h2>

          <!-- Opciones: 1 col en móvil, 2 col en sm+ -->
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <button v-for="opcion in pregunta.opciones" :key="opcion.id"
              @click="seleccionarOpcion(opcion)"
              :disabled="enviando"
              class="bg-white/10 border border-white/20 rounded-xl p-4 text-left
                     hover:bg-white/20 transition-all cursor-pointer
                     disabled:opacity-50 disabled:cursor-not-allowed
                     flex items-start gap-3">
              <span class="font-black text-2xl text-blue-300 flex-shrink-0">
                {{ opcion.letra }}
              </span>
              <span class="text-sm font-semibold leading-snug">{{ opcion.texto }}</span>
            </button>
          </div>
        </div>
      </div>

      <!-- ══ Enviando ══ -->
      <div v-else-if="enviando" class="text-center py-20">
        <p class="text-xl sm:text-2xl animate-pulse">Analizando tus hábitos con IA...</p>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../api/axios'
import NavBar from '../components/NavBar.vue'

const route = useRoute()
const router = useRouter()
const test = ref(null)
const preguntaActual = ref(0)
const respuestas = ref([])
const testIniciado = ref(false)
const enviando = ref(false)

const categorias = [
  {
    titulo: 'ORGANIZACIÓN Y GESTIÓN DEL TIEMPO',
    items: ['Procrastinación', 'Falta de planificación', 'Estudiar solo antes de los exámenes']
  },
  {
    titulo: 'MÉTODOS Y TÉCNICAS DE ESTUDIO',
    items: ['Estudiar con distracciones', 'Multitarea', 'No tomar apuntes']
  },
  {
    titulo: 'ENTORNO Y ACTITUDES PERSONALES',
    items: ['Espacios incómodos', 'Falta de disciplina personal', 'Desmotivación']
  }
]

const pregunta = computed(() => test.value?.preguntas[preguntaActual.value])

onMounted(async () => {
  const { data } = await api.get(`/tests/${route.params.id}/`)
  test.value = data
})

async function seleccionarOpcion(opcion) {
  respuestas.value.push({
    pregunta_id: pregunta.value.id,
    opcion_id: opcion.id
  })

  if (preguntaActual.value < test.value.preguntas.length - 1) {
    preguntaActual.value++
  } else {
    enviando.value = true
    try {
      const { data } = await api.post('/resultados/enviar/', {
        test_id: test.value.id,
        respuestas: respuestas.value
      })
      router.push(`/resultado/${data.uuid}`)
    } catch (e) {
      console.error('Error al enviar respuestas:', e.response?.data || e)
      enviando.value = false
    }
  }
}
</script>