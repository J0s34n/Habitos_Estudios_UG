<template>
  <div class="min-h-screen text-white">
    <NavBar />
    <div class="px-4 sm:px-6 lg:px-12 pb-8 w-full">

      <!-- Header -->
      <div class="flex justify-between items-center mb-8">
        <div>
          <h1 class="text-3xl font-black">📝 TESTS</h1>
          <p class="text-blue-300 text-sm mt-1">
            {{ tests.length }} tests configurados •
            {{ tests.filter(t => t.activo).length }} activos
          </p>
        </div>
        <button @click="abrirModalNuevo"
          class="bg-cyan-500 hover:bg-cyan-400 text-black font-black px-6 py-3
                 rounded-full transition-all flex items-center gap-2">
          + Crear Nuevo Test
        </button>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="text-center py-20">
        <p class="text-blue-300 animate-pulse">Cargando tests...</p>
      </div>

      <!-- Grid de tests -->
      <div v-else class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
        <div v-for="test in tests" :key="test.id"
          class="bg-white/10 border rounded-2xl overflow-hidden transition-all"
          :class="test.activo
            ? 'border-green-400/40 hover:border-green-400/70'
            : 'border-white/10 opacity-60 hover:opacity-80'">

          <!-- Header tarjeta -->
          <div class="px-5 pt-5 pb-3 flex justify-between items-start">
            <div>
              <span class="text-xs font-bold px-2 py-1 rounded-full"
                :class="test.activo ? 'bg-green-500/20 text-green-400' : 'bg-gray-500/20 text-gray-400'">
                {{ test.activo ? '● ACTIVO' : '○ INACTIVO' }}
              </span>
              <h3 class="font-black text-lg mt-2">{{ test.nombre }}</h3>
              <p class="text-blue-300 text-xs mt-1">
                Creado: {{ formatFecha(test.fecha_creacion) }} •
                Modificado: {{ formatFecha(test.fecha_modificacion) }}
              </p>
            </div>
          </div>

          <!-- Descripción -->
          <p class="px-5 text-sm text-white/70 leading-relaxed">{{ test.descripcion }}</p>

          <!-- Stats -->
          <div class="px-5 py-4 grid grid-cols-3 gap-2 text-center">
            <div class="bg-white/5 rounded-lg p-2">
              <p class="font-black text-xl text-cyan-400">{{ test.total_preguntas }}</p>
              <p class="text-xs text-white/50">Preguntas</p>
            </div>
            <div class="bg-white/5 rounded-lg p-2">
              <p class="font-black text-xl text-cyan-400">
                {{ contarArea(test, 'tiempo') }}
              </p>
              <p class="text-xs text-white/50">Tiempo</p>
            </div>
            <div class="bg-white/5 rounded-lg p-2">
              <p class="font-black text-xl text-cyan-400">
                {{ contarArea(test, 'metodos') }}
              </p>
              <p class="text-xs text-white/50">Métodos</p>
            </div>
          </div>

          <!-- Áreas evaluadas -->
          <div class="px-5 pb-3 space-y-1">
            <p class="text-xs text-white/40 font-bold mb-2">ÁREAS EVALUADAS</p>
            <div v-for="area in areas" :key="area.key"
              class="flex items-center gap-2 text-xs">
              <span class="w-2 h-2 rounded-full" :class="area.color" />
              <span class="text-white/70">{{ area.label }}</span>
            </div>
          </div>

          <!-- Acciones -->
          <div class="px-5 pb-5 grid grid-cols-2 gap-2 mt-2">
            <button @click="abrirModalEditar(test)"
              class="bg-blue-600 hover:bg-blue-500 text-white font-bold py-2 rounded-lg
                     text-sm transition-all flex items-center justify-center gap-1">
              ✏️ Editar
            </button>
            <button @click="verPreguntas(test)"
              class="bg-white/10 hover:bg-white/20 text-white font-bold py-2 rounded-lg
                     text-sm transition-all flex items-center justify-center gap-1">
              📋 Preguntas
            </button>
            <button @click="toggleTest(test)"
              class="font-bold py-2 rounded-lg text-sm transition-all col-span-1"
              :class="test.activo
                ? 'bg-yellow-600/30 hover:bg-yellow-600/50 text-yellow-400'
                : 'bg-green-600/30 hover:bg-green-600/50 text-green-400'">
              {{ test.activo ? '⏸ Desactivar' : '▶ Activar' }}
            </button>
            <button @click="confirmarEliminar(test)"
              class="bg-red-600/30 hover:bg-red-600/50 text-red-400 font-bold py-2
                     rounded-lg text-sm transition-all">
              🗑 Eliminar
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- ═══════════════════════════════════════════════ -->
    <!-- MODAL: Crear / Editar Test                      -->
    <!-- ═══════════════════════════════════════════════ -->
    <div v-if="modalTest" class="fixed inset-0 bg-black/70 flex items-start justify-center
                                  z-50 overflow-y-auto py-8 px-4">
      <div class="bg-gray-900 border border-white/20 rounded-2xl w-full max-w-3xl p-8">
        <div class="flex justify-between items-center mb-6">
          <h2 class="text-2xl font-black">
            {{ editandoTest ? '✏️ Editar Test' : '➕ Nuevo Test' }}
          </h2>
          <button @click="cerrarModal" class="text-white/50 hover:text-white text-2xl">✕</button>
        </div>

        <!-- Info básica -->
        <div class="space-y-4 mb-8">
          <div>
            <label class="block text-sm font-bold mb-2 text-blue-300">NOMBRE DEL TEST</label>
            <input v-model="formTest.nombre" type="text"
              class="w-full bg-white/5 border border-white/20 rounded-lg py-3 px-4
                     text-white focus:outline-none focus:border-cyan-400" />
          </div>
          <div>
            <label class="block text-sm font-bold mb-2 text-blue-300">DESCRIPCIÓN</label>
            <textarea v-model="formTest.descripcion" rows="3"
              class="w-full bg-white/5 border border-white/20 rounded-lg py-3 px-4
                     text-white focus:outline-none focus:border-cyan-400 resize-none" />
          </div>
          <div class="flex items-center gap-3">
            <input type="checkbox" v-model="formTest.activo" id="activo"
              class="w-5 h-5 accent-cyan-400" />
            <label for="activo" class="font-bold text-sm">Test activo (visible para estudiantes)</label>
          </div>
        </div>

        <!-- Preguntas -->
        <div class="mb-6">
          <div class="flex justify-between items-center mb-4">
            <h3 class="font-black text-lg">PREGUNTAS ({{ formTest.preguntas.length }})</h3>
            <button @click="agregarPregunta"
              class="bg-cyan-500/20 hover:bg-cyan-500/40 text-cyan-400 font-bold
                     px-4 py-2 rounded-lg text-sm transition-all">
              + Agregar Pregunta
            </button>
          </div>

          <div v-if="formTest.preguntas.length === 0"
            class="text-center py-8 text-white/40 border border-dashed border-white/20 rounded-xl">
            Sin preguntas aún. Haz clic en "Agregar Pregunta".
          </div>

          <!-- Lista de preguntas -->
          <div class="space-y-6">
            <div v-for="(preg, pi) in formTest.preguntas" :key="pi"
              class="bg-white/5 border border-white/10 rounded-xl p-5">

              <div class="flex justify-between items-start mb-3">
                <span class="text-cyan-400 font-black text-sm">PREGUNTA {{ pi + 1 }}</span>
                <button @click="eliminarPregunta(pi)"
                  class="text-red-400 hover:text-red-300 text-sm">✕ Eliminar</button>
              </div>

              <div class="space-y-3 mb-4">
                <input v-model="preg.texto" type="text" placeholder="Texto de la pregunta..."
                  class="w-full bg-white/5 border border-white/20 rounded-lg py-2 px-3
                         text-white text-sm focus:outline-none focus:border-cyan-400" />

                <div class="flex gap-3">
                  <div class="flex-1">
                    <label class="text-xs text-white/50 mb-1 block">ÁREA</label>
                    <select v-model="preg.area"
                      class="w-full bg-gray-800 border border-white/20 rounded-lg py-2 px-3
                             text-white text-sm focus:outline-none focus:border-cyan-400">
                      <option value="tiempo">Organización y Gestión del Tiempo</option>
                      <option value="metodos">Métodos y Técnicas de Estudio</option>
                      <option value="entorno">Entorno y Actitudes Personales</option>
                    </select>
                  </div>
                  <div class="w-24">
                    <label class="text-xs text-white/50 mb-1 block">ORDEN</label>
                    <input v-model.number="preg.orden" type="number" min="0"
                      class="w-full bg-white/5 border border-white/20 rounded-lg py-2 px-3
                             text-white text-sm focus:outline-none focus:border-cyan-400" />
                  </div>
                </div>
              </div>

              <!-- Opciones -->
              <div>
                <div class="flex justify-between items-center mb-2">
                  <span class="text-xs font-bold text-white/50">OPCIONES DE RESPUESTA</span>
                  <button @click="agregarOpcion(pi)"
                    class="text-xs text-cyan-400 hover:text-cyan-300">+ Opción</button>
                </div>

                <div v-for="(op, oi) in preg.opciones" :key="oi"
                  class="flex gap-2 mb-2 items-center">
                  <span class="w-6 text-center font-black text-white/50 text-sm">{{ op.letra }}</span>
                  <input v-model="op.texto" type="text" placeholder="Texto de la opción..."
                    class="flex-1 bg-white/5 border border-white/20 rounded-lg py-2 px-3
                           text-white text-xs focus:outline-none focus:border-cyan-400" />
                  <div class="flex flex-col items-center">
                    <span class="text-xs text-white/40 mb-1">Peso</span>
                    <select v-model.number="op.peso"
                      class="bg-gray-800 border border-white/20 rounded-lg py-2 px-2
                             text-white text-xs w-16 focus:outline-none"
                      :title="pesoLabel(op.peso)">
                      <option :value="1">1 ✓</option>
                      <option :value="2">2 ~</option>
                      <option :value="3">3 !</option>
                      <option :value="4">4 ✗</option>
                    </select>
                  </div>
                  <button @click="eliminarOpcion(pi, oi)"
                    class="text-red-400 hover:text-red-300 text-sm px-1">✕</button>
                </div>

                <p class="text-xs text-white/30 mt-1">
                  Peso: 1=Óptimo · 2=Regular · 3=Deficiente · 4=Crítico
                </p>
              </div>
            </div>
          </div>
        </div>

        <!-- Botones guardar -->
        <div class="flex gap-3 pt-4 border-t border-white/10">
          <button @click="guardarTest" :disabled="guardando"
            class="flex-1 bg-cyan-500 hover:bg-cyan-400 text-black font-black py-3
                   rounded-full transition-all disabled:opacity-50">
            {{ guardando ? 'Guardando...' : editandoTest ? '💾 Guardar Cambios' : '✅ Crear Test' }}
          </button>
          <button @click="cerrarModal"
            class="px-8 border border-white/20 text-white font-bold py-3
                   rounded-full hover:bg-white/10 transition-all">
            Cancelar
          </button>
        </div>
        <p v-if="errorModal" class="text-red-400 text-sm mt-3 text-center">{{ errorModal }}</p>
      </div>
    </div>

    <!-- Modal confirmación eliminar -->
    <div v-if="modalEliminar" class="fixed inset-0 bg-black/70 flex items-center justify-center z-50">
      <div class="bg-gray-900 border border-red-500/40 rounded-2xl p-8 max-w-sm w-full mx-4">
        <h3 class="text-xl font-black mb-3">¿Eliminar test?</h3>
        <p class="text-white/70 mb-6">
          Esto eliminará <strong>"{{ testAEliminar?.nombre }}"</strong> y todas sus preguntas.
          Esta acción no se puede deshacer.
        </p>
        <div class="flex gap-3">
          <button @click="eliminarTest"
            class="flex-1 bg-red-600 hover:bg-red-500 text-white font-black py-3 rounded-full">
            Sí, eliminar
          </button>
          <button @click="modalEliminar = false"
            class="flex-1 border border-white/20 text-white font-bold py-3 rounded-full
                   hover:bg-white/10">
            Cancelar
          </button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import NavBar from '../components/NavBar.vue'
import api from '../api/axios'

const router = useRouter()
const tests = ref([])
const loading = ref(true)
const modalTest = ref(false)
const modalEliminar = ref(false)
const editandoTest = ref(null)
const testAEliminar = ref(null)
const guardando = ref(false)
const errorModal = ref('')

const areas = [
  { key: 'tiempo', label: 'Organización y Gestión del Tiempo', color: 'bg-cyan-400' },
  { key: 'metodos', label: 'Métodos y Técnicas de Estudio', color: 'bg-blue-400' },
  { key: 'entorno', label: 'Entorno y Actitudes Personales', color: 'bg-indigo-400' },
]

const formTest = ref(testVacio())

function testVacio() {
  return {
    nombre: '',
    descripcion: '',
    activo: true,
    preguntas: []
  }
}

function preguntaVacia(orden = 0) {
  return {
    texto: '',
    area: 'tiempo',
    orden,
    opciones: [
      { letra: 'A', texto: '', peso: 1 },
      { letra: 'B', texto: '', peso: 2 },
      { letra: 'C', texto: '', peso: 3 },
      { letra: 'D', texto: '', peso: 4 },
    ]
  }
}

onMounted(cargarTests)

async function cargarTests() {
  loading.value = true
  try {
    const { data } = await api.get('/tests/')
    tests.value = data
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

function abrirModalNuevo() {
  editandoTest.value = null
  formTest.value = testVacio()
  errorModal.value = ''
  modalTest.value = true
}

function abrirModalEditar(test) {
  editandoTest.value = test
  // Clonar profundo para no mutar el original
  formTest.value = {
    nombre: test.nombre,
    descripcion: test.descripcion,
    activo: test.activo,
    preguntas: test.preguntas.map(p => ({
      id: p.id,
      texto: p.texto,
      area: p.area,
      orden: p.orden,
      opciones: p.opciones.map(o => ({ id: o.id, letra: o.letra, texto: o.texto, peso: o.peso }))
    }))
  }
  errorModal.value = ''
  modalTest.value = true
}

function cerrarModal() {
  modalTest.value = false
  editandoTest.value = null
  errorModal.value = ''
}

function agregarPregunta() {
  formTest.value.preguntas.push(preguntaVacia(formTest.value.preguntas.length + 1))
}

function eliminarPregunta(idx) {
  formTest.value.preguntas.splice(idx, 1)
}

function agregarOpcion(pregIdx) {
  const letras = ['A','B','C','D','E','F']
  const preg = formTest.value.preguntas[pregIdx]
  const letra = letras[preg.opciones.length] || String(preg.opciones.length + 1)
  preg.opciones.push({ letra, texto: '', peso: 2 })
}

function eliminarOpcion(pregIdx, opIdx) {
  formTest.value.preguntas[pregIdx].opciones.splice(opIdx, 1)
}

function pesoLabel(peso) {
  return { 1: 'Óptimo', 2: 'Regular', 3: 'Deficiente', 4: 'Crítico' }[peso]
}

async function guardarTest() {
  if (!formTest.value.nombre.trim()) {
    errorModal.value = 'El nombre del test es obligatorio.'
    return
  }
  errorModal.value = ''
  guardando.value = true
  try {
    if (editandoTest.value) {
      await api.put(`/tests/${editandoTest.value.id}/editar/`, formTest.value)
    } else {
      await api.post('/tests/crear/', formTest.value)
    }
    await cargarTests()
    cerrarModal()
  } catch (e) {
    errorModal.value = e.response?.data
      ? JSON.stringify(e.response.data)
      : 'Error al guardar el test.'
  } finally {
    guardando.value = false
  }
}

async function toggleTest(test) {
  try {
    const { data } = await api.patch(`/tests/${test.id}/toggle/`)
    test.activo = data.activo
  } catch (e) {
    console.error(e)
  }
}

function confirmarEliminar(test) {
  testAEliminar.value = test
  modalEliminar.value = true
}

async function eliminarTest() {
  try {
    await api.delete(`/tests/${testAEliminar.value.id}/editar/`)
    await cargarTests()
    modalEliminar.value = false
  } catch (e) {
    console.error(e)
  }
}

function contarArea(test, area) {
  return test.preguntas?.filter(p => p.area === area).length || 0
}

function formatFecha(fecha) {
  return new Date(fecha).toLocaleDateString('es-MX', {
    day: '2-digit', month: 'short', year: 'numeric'
  })
}

function verPreguntas(test) {
  abrirModalEditar(test)
}
</script>