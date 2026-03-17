<template>
  <div class="min-h-screen text-white">
    <NavBar />
    <div class="px-4 sm:px-6 lg:px-12 pb-8 w-full">

      <!-- Header -->
      <div class="flex justify-between items-center mb-8">
        <div>
          <h1 class="text-3xl font-black">📋 RESPUESTAS</h1>
          <p class="text-blue-300 text-sm mt-1">Total: {{ respuestas.length }} respuestas</p>
        </div>
      </div>

      <!-- Filtros -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <div class="bg-white/5 border border-white/10 rounded-xl p-4">
          <label class="text-white/50 text-xs font-bold mb-2 block">🔍 BUSCAR ESTUDIANTE</label>
          <input v-model="filtros.estudiante" type="text"
            class="w-full bg-transparent border border-white/20 rounded-lg py-2 px-3
                   text-white text-sm focus:outline-none focus:border-cyan-400" />
        </div>
        <div class="bg-white/5 border border-white/10 rounded-xl p-4">
          <label class="text-white/50 text-xs font-bold mb-2 block">⚠️ ÁREA DÉBIL</label>
          <select v-model="filtros.area"
            class="w-full bg-gray-800 border border-white/20 rounded-lg py-2 px-3
                   text-white text-sm focus:outline-none focus:border-cyan-400">
            <option value="">Todas</option>
            <option value="tiempo">Gestión del Tiempo</option>
            <option value="metodos">Métodos de Estudio</option>
            <option value="entorno">Entorno Personal</option>
          </select>
        </div>
        <div class="bg-white/5 border border-white/10 rounded-xl p-4">
          <label class="text-white/50 text-xs font-bold mb-2 block">📊 PORCENTAJE MÍNIMO</label>
          <input v-model.number="filtros.porcentaje" type="number" min="0" max="100"
            placeholder="0"
            class="w-full bg-transparent border border-white/20 rounded-lg py-2 px-3
                   text-white text-sm focus:outline-none focus:border-cyan-400" />
        </div>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="text-center py-20">
        <p class="text-blue-300 animate-pulse">Cargando respuestas...</p>
      </div>

      <!-- Tabla -->
      <div v-else class="bg-white/5 border border-white/10 rounded-2xl overflow-hidden">
        <div class="overflow-x-auto">
        
        <div class="flex justify-between items-center px-6 py-4 border-b border-white/10">
          <h2 class="font-black">Listado de Respuestas</h2>
          <span class="text-white/40 text-sm">
            Mostrando {{ respuestasFiltradas.length }} de {{ respuestas.length }}
          </span>
        </div>

        <div v-if="respuestasFiltradas.length === 0"
          class="text-center py-16 text-white/40">
          No hay respuestas que coincidan con los filtros.
        </div>

        <table v-else class="w-full text-sm min-w-[640px]">
          <thead class="bg-blue-900/40">
            <tr>
              <th class="p-4 text-left text-white/60 font-bold">#</th>
              <th class="p-4 text-left text-white/60 font-bold">Estudiante</th>
              <th class="p-4 text-left text-white/60 font-bold">Test</th>
              <th class="p-4 text-left text-white/60 font-bold">Área Débil</th>
              <th class="p-4 text-left text-white/60 font-bold">% Debilidad</th>
              <th class="p-4 text-left text-white/60 font-bold">Fecha</th>
              <th class="p-4 text-left text-white/60 font-bold">Detalles</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(r, i) in paginadas" :key="r.id"
              class="border-t border-white/5 hover:bg-white/5 transition-all">
              <td class="p-4 text-white/40">{{ (paginaActual - 1) * porPagina + i + 1 }}</td>
              <td class="p-4 text-white font-semibold">{{ r.usuario_nombre || '—' }}</td>
              <td class="p-4 text-white/70">{{ r.test_nombre }}</td>
              <td class="p-4">
                <span class="px-2 py-1 rounded-full text-xs font-bold capitalize"
                  :class="colorArea(r.area_debil_principal)">
                  {{ labelArea(r.area_debil_principal) }}
                </span>
              </td>
              <td class="p-4">
                <span class="font-black"
                  :class="maxScore(r) >= 65 ? 'text-red-400' : maxScore(r) >= 40 ? 'text-yellow-400' : 'text-green-400'">
                  {{ maxScore(r) }}%
                </span>
              </td>
              <td class="p-4 text-white/50 text-xs">{{ formatFecha(r.fecha) }}</td>
              <td class="p-4">
                <button @click="verDetalle(r)"
                  class="text-cyan-400 hover:text-cyan-300 text-xs font-bold transition-all">
                  Ver →
                </button>
              </td>
            </tr>
          </tbody>
        </table>
        </div>
        <!-- Paginación -->
        <div v-if="totalPaginas > 1"
          class="flex justify-between items-center px-6 py-4 border-t border-white/10">
          <button @click="paginaActual--" :disabled="paginaActual === 1"
            class="text-cyan-400 hover:text-cyan-300 disabled:opacity-30 disabled:cursor-not-allowed">
            ← Anterior
          </button>
          <span class="text-white/50 text-sm">
            Página {{ paginaActual }} de {{ totalPaginas }}
          </span>
          <button @click="paginaActual++" :disabled="paginaActual === totalPaginas"
            class="text-cyan-400 hover:text-cyan-300 disabled:opacity-30 disabled:cursor-not-allowed">
            Siguiente →
          </button>
        </div>
      </div>
    </div>

    <!-- Modal detalle resultado -->
    <div v-if="detalleSeleccionado"
      class="fixed inset-0 bg-black/70 flex items-center justify-center z-50 px-4"
      @click.self="detalleSeleccionado = null">
      <div class="bg-gray-900 border border-white/20 rounded-2xl p-8 max-w-lg w-full">
        <div class="flex justify-between items-center mb-6">
          <h2 class="text-xl font-black">Detalle de Resultado</h2>
          <button @click="detalleSeleccionado = null"
            class="text-white/50 hover:text-white text-xl">✕</button>
        </div>

        <div class="space-y-3 mb-6">
          <div class="flex justify-between py-2 border-b border-white/10">
            <span class="text-white/50 text-sm">Test</span>
            <span class="text-white font-bold">{{ detalleSeleccionado.test_nombre }}</span>
          </div>
          <div class="flex justify-between py-2 border-b border-white/10">
            <span class="text-white/50 text-sm">Fecha</span>
            <span class="text-white/70">{{ formatFecha(detalleSeleccionado.fecha) }}</span>
          </div>
          <div class="flex justify-between py-2 border-b border-white/10">
            <span class="text-white/50 text-sm">Área débil principal</span>
            <span class="capitalize font-bold"
              :class="colorAreaTexto(detalleSeleccionado.area_debil_principal)">
              {{ labelArea(detalleSeleccionado.area_debil_principal) }}
            </span>
          </div>
        </div>

        <!-- Scores -->
        <h3 class="font-black text-sm mb-3 text-white/70">SCORES POR ÁREA</h3>
        <div class="space-y-3 mb-6">
          <div v-for="area in [
            { label: 'Gestión del Tiempo', valor: detalleSeleccionado.score_tiempo, color: 'bg-cyan-400' },
            { label: 'Métodos de Estudio', valor: detalleSeleccionado.score_metodos, color: 'bg-blue-400' },
            { label: 'Entorno Personal', valor: detalleSeleccionado.score_entorno, color: 'bg-indigo-400' },
          ]" :key="area.label">
            <div class="flex justify-between text-sm mb-1">
              <span class="text-white/70">{{ area.label }}</span>
              <span class="font-black text-white">{{ area.valor }}%</span>
            </div>
            <div class="w-full bg-white/10 rounded-full h-2">
              <div :class="area.color" class="h-2 rounded-full"
                :style="`width: ${area.valor}%`" />
            </div>
          </div>
        </div>

        <!-- Recomendaciones -->
        <h3 class="font-black text-sm mb-3 text-white/70">RECOMENDACIONES GENERADAS</h3>
        <div class="space-y-2 max-h-40 overflow-y-auto">
          <div v-for="rec in detalleSeleccionado.recomendaciones" :key="rec.texto"
            class="border-l-4 pl-3 py-1 text-xs text-white/70"
            :class="rec.nivel === 'alta' ? 'border-red-400' : rec.nivel === 'media' ? 'border-yellow-400' : 'border-green-400'">
            <span class="font-bold capitalize text-white/90">{{ rec.area }}:</span> {{ rec.texto }}
          </div>
        </div>

        <button @click="detalleSeleccionado = null"
          class="w-full mt-6 border border-white/20 text-white font-bold py-3
                 rounded-full hover:bg-white/10 transition-all">
          Cerrar
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import NavBar from '../components/NavBar.vue'
import api from '../api/axios'

const respuestas = ref([])
const loading = ref(true)
const detalleSeleccionado = ref(null)
const paginaActual = ref(1)
const porPagina = 8

const filtros = ref({
  estudiante: '',
  area: '',
  porcentaje: 0,
})

onMounted(async () => {
  try {
    const { data } = await api.get('/resultados/todos/')
    respuestas.value = data
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
})

const respuestasFiltradas = computed(() => {
  return respuestas.value.filter(r => {
    const matchArea = !filtros.value.area || r.area_debil_principal === filtros.value.area
    const matchPorcentaje = maxScore(r) >= (filtros.value.porcentaje || 0)
    return matchArea && matchPorcentaje
  })
})

const totalPaginas = computed(() =>
  Math.ceil(respuestasFiltradas.value.length / porPagina)
)

const paginadas = computed(() => {
  const inicio = (paginaActual.value - 1) * porPagina
  return respuestasFiltradas.value.slice(inicio, inicio + porPagina)
})

function verDetalle(r) {
  detalleSeleccionado.value = r
}

function maxScore(r) {
  return Math.max(r.score_tiempo, r.score_metodos, r.score_entorno)
}

function labelArea(area) {
  return { tiempo: 'Tiempo', metodos: 'Métodos', entorno: 'Entorno' }[area] || area
}

function colorArea(area) {
  return {
    tiempo: 'bg-cyan-500/20 text-cyan-400',
    metodos: 'bg-blue-500/20 text-blue-400',
    entorno: 'bg-indigo-500/20 text-indigo-400',
  }[area] || 'bg-white/10 text-white/50'
}

function colorAreaTexto(area) {
  return {
    tiempo: 'text-cyan-400',
    metodos: 'text-blue-400',
    entorno: 'text-indigo-400',
  }[area] || 'text-white'
}

function formatFecha(fecha) {
  return new Date(fecha).toLocaleDateString('es-MX', {
    day: '2-digit', month: 'short', year: 'numeric'
  })
}
</script>
