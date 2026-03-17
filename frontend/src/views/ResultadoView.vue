<template>
  <div class="min-h-screen p-8 text-white" v-if="resultado">
    <NavBar />
    <h1 class="text-3xl font-black text-center mb-8">RESULTADO DE TEST</h1>

    <div class="w-full bg-white text-black rounded-2xl p-8">
      <div class="flex flex-col md:flex-row gap-8 items-center">
        <!-- Análisis -->
        <div class="flex-1">
          <p class="font-black text-lg mb-4 leading-relaxed">
            DE ACUERDO A TUS RESPUESTAS, 
            <span class="text-blue-700">{{ textoAnalisis }}</span>
          </p>
          <div class="mt-6 space-y-3">
            <h3 class="font-bold text-gray-700">Recomendaciones personalizadas:</h3>
            <div v-for="rec in resultado.recomendaciones" :key="rec.texto"
              class="border-l-4 pl-3 py-1 text-sm"
              :class="nivelColor(rec.nivel)">
              <span class="font-semibold capitalize">{{ rec.area }}:</span> {{ rec.texto }}
            </div>
          </div>
        </div>

        <!-- Gráfica de pastel -->
        <div class="w-64">
          <Pie :data="chartData" :options="chartOptions" />
          <div class="mt-4 text-xs space-y-1">
            <div class="flex justify-between">
              <span>⏱ Tiempo</span>
              <span class="font-bold">{{ resultado.score_tiempo }}%</span>
            </div>
            <div class="flex justify-between">
              <span>📚 Métodos</span>
              <span class="font-bold">{{ resultado.score_metodos }}%</span>
            </div>
            <div class="flex justify-between">
              <span>🏠 Entorno</span>
              <span class="font-bold">{{ resultado.score_entorno }}%</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="text-center mt-8">
      <RouterLink to="/menu"
        class="bg-white text-blue-900 font-bold py-3 px-8 rounded-full
               hover:bg-blue-100 transition-all">
        REGRESAR AL MENÚ →
      </RouterLink>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { Pie } from 'vue-chartjs'
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js'
import api from '../api/axios'
import NavBar from '../components/NavBar.vue'

ChartJS.register(ArcElement, Tooltip, Legend)

const route = useRoute()
const resultado = ref(null)

const textoAnalisis = computed(() => {
  if (!resultado.value) return ''
  const area = resultado.value.area_debil_principal
  const textos = {
    tiempo: 'el tiempo es una parte crucial que te limita a estudiar de manera óptima.',
    metodos: 'tus métodos de estudio necesitan mejoras para optimizar tu aprendizaje.',
    entorno: 'tu entorno y actitud personal son los principales obstáculos en tu estudio.'
  }
  return textos[area] || ''
})

const chartData = computed(() => ({
  labels: ['Tiempo', 'Métodos', 'Entorno'],
  datasets: [{
    data: [
      resultado.value?.score_tiempo,
      resultado.value?.score_metodos,
      resultado.value?.score_entorno
    ],
    backgroundColor: ['#00bcd4', '#0d47a1', '#1565c0'],
  }]
}))

const chartOptions = {
  responsive: true,
  plugins: { legend: { position: 'bottom' } }
}

function nivelColor(nivel) {
  return {
    'alta': 'border-red-500 text-red-700',
    'media': 'border-yellow-500 text-yellow-700',
    'baja': 'border-green-500 text-green-700',
  }[nivel]
}

onMounted(async () => {
  try {
      const { data } = await api.get(`/resultados/mis-resultados/${route.params.id}/`)
      resultado.value = data
    } catch (e) {
      router.push('/evaluaciones')
    }
  })
</script>