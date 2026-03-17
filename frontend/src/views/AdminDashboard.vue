<template>
  <div class="min-h-screen text-white">
    <NavBar />
    
    <div class="w-full px-4 sm:px-6 lg:px-10 pb-8">
      <h1 class="text-3xl sm:text-4xl font-black text-center mb-8">
        PANEL DE ADMINISTRACIÓN
      </h1>

      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">

        <!-- Respuestas -->
        <RouterLink to="/admin/respuestas"
          class="bg-white/10 border border-white/20 rounded-2xl p-6
                 hover:bg-white/20 transition-all">
          <h2 class="font-black text-lg mb-4">RESPUESTAS:
            <span class="text-cyan-400">{{ stats.totalRespuestas }}</span>
          </h2>
          <div class="flex gap-2 items-end h-20">
            <div v-if="stats.porTest.length === 0"
              class="text-white/30 text-sm w-full text-center">Sin datos aún</div>
            <div v-for="test in stats.porTest" :key="test.nombre"
              class="flex flex-col items-center flex-1 min-w-0">
              <div class="w-full bg-blue-400/60 rounded-t-sm transition-all"
                :style="`height: ${(test.total / Math.max(...stats.porTest.map(t=>t.total), 1)) * 70}px`" />
              <span class="text-xs mt-1 text-blue-200 truncate w-full text-center">
                {{ test.nombre.split(' ')[0] }}
              </span>
            </div>
          </div>
        </RouterLink>

        <!-- Reportes -->
        <RouterLink to="/admin/reportes"
          class="bg-white/10 border border-white/20 rounded-2xl p-6
                 hover:bg-white/20 transition-all">
          <h2 class="font-black text-lg mb-4">REPORTES:
            <span class="text-cyan-400">{{ stats.totalReportes }}</span>
          </h2>
          <div class="grid grid-cols-2 gap-3 mt-2">
            <div v-for="i in 4" :key="i" class="bg-white/10 rounded-lg h-12" />
          </div>
        </RouterLink>

        <!-- Tests -->
        <RouterLink to="/admin/tests"
          class="bg-white/10 border border-white/20 rounded-2xl p-6
                 hover:bg-white/20 transition-all">
          <h2 class="font-black text-lg mb-4">TEST:
            <span class="text-cyan-400">{{ stats.totalTests }}</span>
          </h2>
          <div class="grid grid-cols-2 gap-3 mt-2">
            <div v-for="i in 4" :key="i" class="bg-white/10 rounded-lg h-12" />
          </div>
        </RouterLink>

        <!-- Estudiantes -->
        <RouterLink to="/admin/estudiantes"
          class="bg-white/10 border border-white/20 rounded-2xl p-6
                 hover:bg-white/20 transition-all">
          <h2 class="font-black text-lg mb-2">ESTUDIANTES:
            <span class="text-cyan-400">{{ stats.totalEstudiantes }}</span>
          </h2>
          <div class="text-6xl mt-4 text-center">👥</div>
        </RouterLink>

        <!-- Quejas — ocupa 2 columnas en sm+  -->
        <RouterLink to="/admin/quejas"
          class="bg-white/10 border border-white/20 rounded-2xl p-6
                 hover:bg-white/20 transition-all sm:col-span-2 xl:col-span-2">
          <h2 class="font-black text-lg mb-2">SUGERENCIAS Y QUEJAS:
            <span class="text-cyan-400">{{ stats.totalQuejas }}</span>
          </h2>
          <p class="text-white/40 text-sm mt-2">
            Ver todas las quejas y sugerencias de los estudiantes →
          </p>
        </RouterLink>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import api from '../api/axios'
import PageContainer from '@/components/PageContainer.vue'
import NavBar from '@/components/NavBar.vue'

const auth = useAuthStore()
const seccion = ref(null)
const respuestas = ref([])

const stats = ref({
  totalRespuestas: 0,
  totalEstudiantes: 0,
  totalTests: 0,
  totalReportes: 0,
  totalQuejas: 0,
  porTest: []
})

onMounted(async () => {
const [resResp, resEst, resQuejas, resTests, resReportes] = await Promise.allSettled([
  api.get('/resultados/todos/'),
  api.get('/usuarios/lista/'),
  api.get('/usuarios/quejas/'),
  api.get('/tests/'),
  api.get('/reportes/'),  
])

  if (resReportes.status === 'fulfilled')
  stats.value.totalReportes = resReportes.value.data.length
  
  if (resResp.status === 'fulfilled') {
    stats.value.totalRespuestas = resResp.value.data.length
    const grupos = {}
    resResp.value.data.forEach(r => {
      grupos[r.test_nombre] = (grupos[r.test_nombre] || 0) + 1
    })
    stats.value.porTest = Object.entries(grupos)
      .map(([nombre, total]) => ({ nombre, total }))
  }

  if (resEst.status === 'fulfilled')
    stats.value.totalEstudiantes = resEst.value.data.length

  if (resTests.status === 'fulfilled')
    stats.value.totalTests = resTests.value.data.length

  if (resQuejas.status === 'fulfilled')
    stats.value.totalQuejas = resQuejas.value.data.length
})
async function cargarRespuestas() {
  if (respuestas.value.length) return
  try {
    const { data } = await api.get('/resultados/todos/')
    respuestas.value = data
  } catch (e) { console.error(e) }
}

function formatFecha(fecha) {
  return new Date(fecha).toLocaleDateString('es-MX', {
    day: '2-digit', month: 'short', year: '2-digit'
  })
}

function maxScore(r) {
  return Math.max(r.score_tiempo, r.score_metodos, r.score_entorno)
}
</script>