<template>
  <div class="min-h-screen text-white">
    <NavBar />
    <div class="px-4 sm:px-6 lg:px-12 pb-8 w-full">

      <!-- Header -->
      <div class="flex justify-between items-center mb-8">
        <div>
          <h1 class="text-3xl font-black">👥 ESTUDIANTES</h1>
          <p class="text-blue-300 text-sm mt-1">{{ estudiantes.length }} estudiantes registrados</p>
        </div>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="text-center py-20">
        <p class="text-blue-300 animate-pulse">Cargando estudiantes...</p>
      </div>

      <!-- Sin estudiantes -->
      <div v-else-if="estudiantes.length === 0"
        class="text-center py-20 border border-dashed border-white/20 rounded-2xl">
        <p class="text-4xl mb-4">👤</p>
        <p class="text-white/50">No hay estudiantes registrados aún.</p>
      </div>

      <!-- Buscador -->
      <div v-else>
        <div class="mb-6">
          <input v-model="busqueda" type="text" placeholder="🔍 Buscar por nombre o email..."
            class="w-full md:w-96 bg-white/5 border border-white/20 rounded-full py-3 px-5
                   text-white placeholder-white/30 focus:outline-none focus:border-cyan-400" />
        </div>

        <!-- Tabla -->
      <div class="bg-white/5 border border-white/10 rounded-2xl overflow-hidden">
        <div class="overflow-x-auto">  
          <table class="w-full text-sm min-w-[640px]">
            <thead class="bg-blue-900/60">
              <tr>
                <th class="p-4 text-left text-white/70 font-bold">#</th>
                <th class="p-4 text-left text-white/70 font-bold">Nombre</th>
                <th class="p-4 text-left text-white/70 font-bold">Usuario</th>
                <th class="p-4 text-left text-white/70 font-bold">Email</th>
                <th class="p-4 text-left text-white/70 font-bold">Registro</th>
                <th class="p-4 text-left text-white/70 font-bold">Tests</th>
                <th class="p-4 text-left text-white/70 font-bold">Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(est, i) in estudiantesFiltrados" :key="est.id"
                class="border-t border-white/5 hover:bg-white/5 transition-all">
                <td class="p-4 text-white/40">{{ i + 1 }}</td>
                <td class="p-4">
                  <p class="font-bold text-white">
                    {{ est.first_name || '—' }} {{ est.primer_apellido || '' }}
                  </p>
                </td>
                <td class="p-4 text-white/70">{{ est.username }}</td>
                <td class="p-4 text-blue-300 text-xs">{{ est.email || '—' }}</td>
                <td class="p-4 text-white/50 text-xs">{{ formatFecha(est.fecha_registro) }}</td>
                <td class="p-4">
                  <span class="bg-cyan-500/20 text-cyan-400 px-2 py-1 rounded-full text-xs font-bold">
                    {{ resultadosPor[est.id] || 0 }} tests
                  </span>
                </td>
                <td class="p-4">
                  <button @click="verDetalle(est)"
                    class="text-blue-300 hover:text-white text-xs font-bold transition-all">
                    Ver detalle →
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        </div>
      </div>
    </div>

    <!-- Modal detalle estudiante -->
    <div v-if="estudianteSeleccionado"
      class="fixed inset-0 bg-black/70 flex items-center justify-center z-50 px-4"
      @click.self="estudianteSeleccionado = null">
      <div class="bg-gray-900 border border-white/20 rounded-2xl p-8 max-w-lg w-full">

        <div class="flex justify-between items-start mb-6">
          <div class="flex items-center gap-4">
            <div class="text-5xl">👤</div>
            <div>
              <h2 class="text-xl font-black">
                {{ estudianteSeleccionado.first_name || estudianteSeleccionado.username }}
                {{ estudianteSeleccionado.primer_apellido || '' }}
              </h2>
              <p class="text-blue-300 text-sm">@{{ estudianteSeleccionado.username }}</p>
            </div>
          </div>
          <button @click="estudianteSeleccionado = null"
            class="text-white/50 hover:text-white text-xl">✕</button>
        </div>

        <div class="space-y-3 mb-6">
          <div class="flex justify-between py-2 border-b border-white/10">
            <span class="text-white/50 text-sm">Email</span>
            <span class="text-blue-300 text-sm">{{ estudianteSeleccionado.email || '—' }}</span>
          </div>
          <div class="flex justify-between py-2 border-b border-white/10">
            <span class="text-white/50 text-sm">Matrícula</span>
            <span class="text-white/70 text-sm">{{ estudianteSeleccionado.matricula || '—' }}</span>
          </div>
          <div class="flex justify-between py-2 border-b border-white/10">
            <span class="text-white/50 text-sm">Fecha de registro</span>
            <span class="text-white/70 text-sm">{{ formatFecha(estudianteSeleccionado.fecha_registro) }}</span>
          </div>
          <div class="flex justify-between py-2">
            <span class="text-white/50 text-sm">Tests realizados</span>
            <span class="text-cyan-400 font-black">{{ resultadosPor[estudianteSeleccionado.id] || 0 }}</span>
          </div>
        </div>

        <!-- Resultados del estudiante -->
        <div v-if="resultadosEstudiante.length > 0">
          <h3 class="font-black text-sm mb-3 text-white/70">EVALUACIONES REALIZADAS</h3>
          <div class="space-y-2 max-h-48 overflow-y-auto">
            <div v-for="r in resultadosEstudiante" :key="r.id"
              class="bg-white/5 rounded-lg p-3 flex justify-between items-center">
              <div>
                <p class="text-sm font-bold">{{ r.test_nombre }}</p>
                <p class="text-xs text-white/40">{{ formatFecha(r.fecha) }}</p>
              </div>
              <div class="text-right">
                <p class="text-xs text-white/50 capitalize">{{ r.area_debil_principal }}</p>
                <p class="text-cyan-400 font-black text-sm">
                  {{ Math.max(r.score_tiempo, r.score_metodos, r.score_entorno) }}%
                </p>
              </div>
            </div>
          </div>
        </div>
        <!-- Cambiar rol --> 
        <div class="mt-4 pt-4 border-t border-white/10">
          <p class="text-white/40 text-xs mb-3 font-bold">GESTIÓN DE ROL</p>
          <button @click="cambiarRol(estudianteSeleccionado)"
            :class="estudianteSeleccionado.rol === 'estudiante'
              ? 'bg-cyan-500/20 hover:bg-cyan-500/40 text-cyan-400 border border-cyan-500/40'
              : 'bg-red-500/20 hover:bg-red-500/40 text-red-400 border border-red-500/40'"
            class="w-full font-bold py-2 rounded-lg text-sm transition-all">
            {{ estudianteSeleccionado.rol === 'estudiante'
              ? '⬆️ Promover a Administrador'
              : '⬇️ Cambiar a Estudiante' }}
          </button>
          <p class="text-white/30 text-xs mt-2 text-center">
            Rol actual: <span class="capitalize font-bold">{{ estudianteSeleccionado.rol }}</span>
          </p>
        </div>

        <button @click="estudianteSeleccionado = null"
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

const estudiantes = ref([])
const todosResultados = ref([])
const loading = ref(true)
const busqueda = ref('')
const estudianteSeleccionado = ref(null)
const resultadosEstudiante = ref([])

const resultadosPor = computed(() => {
  const conteo = {}
  todosResultados.value.forEach(r => {
    if (r.usuario_id) {
      conteo[r.usuario_id] = (conteo[r.usuario_id] || 0) + 1
    }
  })
  return conteo
})

const estudiantesFiltrados = computed(() => {
  if (!busqueda.value) return estudiantes.value
  const q = busqueda.value.toLowerCase()
  return estudiantes.value.filter(e =>
    e.username.toLowerCase().includes(q) ||
    (e.first_name || '').toLowerCase().includes(q) ||
    (e.email || '').toLowerCase().includes(q)
  )
})

onMounted(async () => {
  try {
    const [resEst, resResp] = await Promise.allSettled([
      api.get('/usuarios/lista/'),
      api.get('/resultados/todos/'),
    ])
    if (resEst.status === 'fulfilled') estudiantes.value = resEst.value.data
    if (resResp.status === 'fulfilled') todosResultados.value = resResp.value.data
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
})

async function verDetalle(est) {
  estudianteSeleccionado.value = est
  try {
    const { data } = await api.get('/resultados/todos/')
    resultadosEstudiante.value = data.filter(r => r.usuario_id === est.id)
  } catch (e) {
    console.error(e)
  }
}

function formatFecha(fecha) {
  if (!fecha) return '—'
  return new Date(fecha).toLocaleDateString('es-MX', {
    day: '2-digit', month: 'short', year: 'numeric'
  })
}

async function cambiarRol(est) {
  try {
    const { data } = await api.patch(`/usuarios/${est.id}/cambiar-rol/`)
    est.rol = data.nuevo_rol
    // Actualizar en la lista principal
    const idx = estudiantes.value.findIndex(e => e.id === est.id)
    if (idx !== -1) estudiantes.value[idx].rol = data.rol
    // Recargar lista desde la BD para asegurar consistencia
    const resEst = await api.get('/usuarios/lista/')
    estudiantes.value = resEst.data
    // Actualizar el estudiante seleccionado con la nueva información
    estudianteSeleccionado.value = estudiantes.value.find(e => e.id === est.id) || null
    alert(`Rol cambiado a ${data.nuevo_rol} exitosamente. El usuario debe cerrar sesión y volver a iniciar para que el cambio tome efecto.`)
  } catch (e) {
    console.error(e)
    alert('Error al cambiar el rol. Intenta de nuevo.')
  }
  }
</script>
