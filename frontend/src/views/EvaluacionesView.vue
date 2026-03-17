<template>
  <div class="min-h-screen p-8 text-white">
    <!-- Header -->
    <div class="flex justify-between items-start mb-8">
      <div>
        <p class="text-xl">HOLA: <strong>{{ auth.user?.first_name || auth.user?.username }}</strong></p>
        <p class="text-blue-300">BIENVENIDO</p>
      </div>
      <div class="bg-amber-700/60 rounded-full px-6 py-3 flex items-center gap-3 border border-amber-500/30">
        <span class="text-2xl">🕐</span>
        <span class="font-black">EVALUACIONES PASADAS</span>
      </div>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="text-center py-20">
      <p class="text-blue-300 animate-pulse text-lg">Cargando evaluaciones...</p>
    </div>

    <!-- Sin resultados -->
    <div v-else-if="resultados.length === 0" class="text-center py-20">
      <p class="text-blue-300 text-lg mb-4">Aún no has realizado ningún test.</p>
      <RouterLink to="/test/1"
        class="bg-white text-blue-900 font-bold py-3 px-8 rounded-full hover:bg-blue-100 transition-all">
        Realizar primer test
      </RouterLink>
    </div>

    <!-- Tarjetas de resultados -->
    <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-5xl">
      <div v-for="resultado in resultados" :key="resultado.id"
        class="bg-white text-black rounded-2xl p-6 shadow-lg">
        <div class="flex justify-between items-start mb-4">
          <h3 class="font-black text-lg">TEST REALIZADO</h3>
          <span class="text-xs text-gray-500">{{ formatFecha(resultado.fecha) }}</span>
        </div>

        <!-- Mini gráfica de barras -->
        <div class="flex items-end gap-2 h-16 mb-4">
          <div v-for="(val, label) in barras(resultado)" :key="label" class="flex flex-col items-center flex-1">
            <div class="w-full rounded-t-sm bg-cyan-400 transition-all"
              :style="`height: ${val}%`" />
            <span class="text-xs mt-1 text-gray-500">{{ label }}</span>
          </div>
        </div>

        <p class="text-sm font-black mb-1">RESUMEN:</p>
        <p class="text-sm text-gray-600">{{ resumen(resultado) }}</p>

        <RouterLink :to="`/resultado/${resultado.uuid}`"
          class="mt-4 inline-block text-blue-700 font-bold text-sm hover:underline">
          Ver detalle →
        </RouterLink>
      </div>
    </div>

    <!-- Navegación -->
    <div class="flex justify-between mt-8 max-w-5xl">
      <RouterLink to="/menu"
        class="bg-white/10 border border-white/20 text-white font-bold py-3 px-6 rounded-full
               hover:bg-white/20 transition-all">
        ← Menú
      </RouterLink>
      <RouterLink to="/test/1"
        class="bg-white text-blue-900 font-bold py-3 px-6 rounded-full
               hover:bg-blue-100 transition-all">
        Nuevo test →
      </RouterLink>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import api from '../api/axios'

const auth = useAuthStore()
const resultados = ref([])
const loading = ref(true)

onMounted(async () => {
  try {
    const { data } = await api.get('/resultados/mis-resultados/')
    resultados.value = data
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
})

function formatFecha(fecha) {
  return new Date(fecha).toLocaleDateString('es-MX', {
    day: '2-digit', month: 'short', year: 'numeric'
  })
}

function barras(r) {
  return {
    'Tiempo': r.score_tiempo,
    'Métodos': r.score_metodos,
    'Entorno': r.score_entorno,
  }
}

function resumen(r) {
  const textos = {
    tiempo: 'Presentaste una debilidad en el manejo del tiempo.',
    metodos: 'Mejora tus métodos y técnicas de estudio.',
    entorno: 'Mejora tu entorno para una mejor calidad de estudio.',
  }
  return textos[r.area_debil_principal] || 'Revisa tus resultados detallados.'
}
</script>