<template>
  <div class="min-h-screen text-white">
    <NavBar />
    <div class="px-4 sm:px-6 lg:px-12 pb-8 w-full">

      <!-- Header -->
      <div class="flex justify-between items-center mb-8">
        <div>
          <h1 class="text-3xl font-black">📬 QUEJAS Y SUGERENCIAS</h1>
          <p class="text-blue-300 text-sm mt-1">
            {{ total }} total •
            {{ sinLeer }} sin leer
          </p>
        </div>
        <!-- Filtros -->
        <div class="flex gap-2">
          <button v-for="f in filtros" :key="f.valor"
            @click="filtroActivo = f.valor"
            :class="filtroActivo === f.valor
              ? 'bg-white text-blue-900 font-black'
              : 'border border-white/30 text-white/70 hover:bg-white/10'"
            class="px-4 py-2 rounded-full text-sm transition-all">
            {{ f.label }}
          </button>
        </div>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="text-center py-20">
        <p class="text-blue-300 animate-pulse">Cargando mensajes...</p>
      </div>

      <!-- Sin resultados -->
      <div v-else-if="listaFiltrada.length === 0"
        class="text-center py-20 border border-dashed border-white/20 rounded-2xl">
        <p class="text-4xl mb-4">📭</p>
        <p class="text-white/50">No hay {{ filtroActivo === 'todos' ? 'mensajes' : filtroActivo + 's' }} aún.</p>
      </div>

      <!-- Lista -->
      <div v-else class="space-y-4">
        <div v-for="queja in listaFiltrada" :key="queja.id"
          class="bg-white/5 border rounded-2xl p-6 transition-all cursor-pointer hover:bg-white/10"
          :class="queja.leida ? 'border-white/10' : 'border-cyan-400/40'"
          @click="abrirDetalle(queja)">

          <div class="flex justify-between items-start">
            <div class="flex items-center gap-3">
              <!-- Badge tipo -->
              <span class="px-3 py-1 rounded-full text-xs font-black"
                :class="queja.tipo === 'queja'
                  ? 'bg-red-500/20 text-red-400'
                  : 'bg-cyan-500/20 text-cyan-400'">
                {{ queja.tipo === 'queja' ? '⚠️ QUEJA' : '💡 SUGERENCIA' }}
              </span>
              <!-- Sin leer -->
              <span v-if="!queja.leida"
                class="w-2 h-2 rounded-full bg-cyan-400 animate-pulse" />
            </div>
            <span class="text-white/40 text-xs">{{ formatFecha(queja.fecha) }}</span>
          </div>

          <p class="mt-3 text-white/80 text-sm leading-relaxed line-clamp-2">
            {{ queja.comentario }}
          </p>

          <div class="mt-3 flex justify-between items-center">
            <span class="text-blue-300 text-xs">📧 {{ queja.email }}</span>
            <button @click.stop="marcarLeida(queja)"
              v-if="!queja.leida"
              class="text-xs text-cyan-400 hover:text-cyan-300 transition-all">
              Marcar como leída ✓
            </button>
            <span v-else class="text-xs text-white/30">Leída ✓</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal detalle -->
    <div v-if="quejaSeleccionada"
      class="fixed inset-0 bg-black/70 flex items-center justify-center z-50 px-4"
      @click.self="quejaSeleccionada = null">
      <div class="bg-gray-900 border border-white/20 rounded-2xl p-8 max-w-lg w-full">

        <div class="flex justify-between items-start mb-6">
          <span class="px-3 py-1 rounded-full text-sm font-black"
            :class="quejaSeleccionada.tipo === 'queja'
              ? 'bg-red-500/20 text-red-400'
              : 'bg-cyan-500/20 text-cyan-400'">
            {{ quejaSeleccionada.tipo === 'queja' ? '⚠️ QUEJA' : '💡 SUGERENCIA' }}
          </span>
          <button @click="quejaSeleccionada = null"
            class="text-white/50 hover:text-white text-xl">✕</button>
        </div>

        <div class="space-y-4">
          <div>
            <p class="text-white/40 text-xs mb-1">COMENTARIO</p>
            <p class="text-white leading-relaxed">{{ quejaSeleccionada.comentario }}</p>
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <p class="text-white/40 text-xs mb-1">EMAIL</p>
              <p class="text-blue-300 text-sm">{{ quejaSeleccionada.email }}</p>
            </div>
            <div>
              <p class="text-white/40 text-xs mb-1">FECHA</p>
              <p class="text-white/70 text-sm">{{ formatFechaCompleta(quejaSeleccionada.fecha) }}</p>
            </div>
          </div>
          <div>
            <p class="text-white/40 text-xs mb-1">ESTADO</p>
            <span class="text-sm"
              :class="quejaSeleccionada.leida ? 'text-white/40' : 'text-cyan-400'">
              {{ quejaSeleccionada.leida ? '✓ Leída' : '● Sin leer' }}
            </span>
          </div>
        </div>

        <div class="flex gap-3 mt-8">
          <button v-if="!quejaSeleccionada.leida"
            @click="marcarLeida(quejaSeleccionada); quejaSeleccionada = null"
            class="flex-1 bg-cyan-500 hover:bg-cyan-400 text-black font-black py-3 rounded-full transition-all">
            Marcar como leída ✓
          </button>
          <button @click="quejaSeleccionada = null"
            class="flex-1 border border-white/20 text-white font-bold py-3 rounded-full
                   hover:bg-white/10 transition-all">
            Cerrar
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import NavBar from '../components/NavBar.vue'
import api from '../api/axios'

const quejas = ref([])
const loading = ref(true)
const filtroActivo = ref('todos')
const quejaSeleccionada = ref(null)

const filtros = [
  { label: 'Todos', valor: 'todos' },
  { label: '⚠️ Quejas', valor: 'queja' },
  { label: '💡 Sugerencias', valor: 'sugerencia' },
  { label: '● Sin leer', valor: 'sin_leer' },
]

const total = computed(() => quejas.value.length)
const sinLeer = computed(() => quejas.value.filter(q => !q.leida).length)

const listaFiltrada = computed(() => {
  if (filtroActivo.value === 'todos') return quejas.value
  if (filtroActivo.value === 'sin_leer') return quejas.value.filter(q => !q.leida)
  return quejas.value.filter(q => q.tipo === filtroActivo.value)
})

onMounted(async () => {
  try {
    const { data } = await api.get('/usuarios/quejas/')
    quejas.value = data
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
})

async function marcarLeida(queja) {
  try {
    await api.patch(`/usuarios/quejas/${queja.id}/`, { leida: true })
    queja.leida = true
  } catch (e) {
    console.error(e)
  }
}

function abrirDetalle(queja) {
  quejaSeleccionada.value = queja
}

function formatFecha(fecha) {
  return new Date(fecha).toLocaleDateString('es-MX', {
    day: '2-digit', month: 'short', year: 'numeric'
  })
}

function formatFechaCompleta(fecha) {
  return new Date(fecha).toLocaleString('es-MX', {
    day: '2-digit', month: 'long', year: 'numeric',
    hour: '2-digit', minute: '2-digit'
  })
}
</script>
