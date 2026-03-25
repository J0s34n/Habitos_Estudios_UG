<template>
  <div class="min-h-screen text-white">
    <NavBar />
    <div class="px-4 sm:px-6 lg:px-12 pb-8 w-full">

      <!-- Header -->
      <div class="flex justify-between items-center mb-8">
        <div>
          <h1 class="text-3xl font-black">📊 REPORTES</h1>
          <p class="text-blue-300 text-sm mt-1">
            {{ reportes.length }} reportes disponibles
            <!-- Nota de versión futura -->
            <span class="ml-2 text-white/30 text-xs">
              · En versiones futuras se podrán personalizar por rango de fechas y filtros
            </span>
          </p>
        </div>
        <button @click="modalGenerar = true"
          class="bg-cyan-500/20 hover:bg-cyan-500/40 border border-cyan-500/50
                 text-cyan-400 font-black px-6 py-3 rounded-full transition-all
                 flex items-center gap-2">
          + Generar Nuevo Reporte
        </button>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="text-center py-20">
        <p class="text-blue-300 animate-pulse">Cargando reportes...</p>
      </div>

      <!-- Sin reportes -->
      <div v-else-if="reportes.length === 0"
        class="text-center py-20 border border-dashed border-white/20 rounded-2xl">
        <p class="text-4xl mb-4">📈</p>
        <p class="text-white/50 mb-4">No hay reportes generados aún.</p>
        <button @click="modalGenerar = true"
          class="bg-cyan-500 hover:bg-cyan-400 text-black font-black px-8 py-3 rounded-full">
          Generar primer reporte
        </button>
      </div>

      <!-- Grid de reportes -->
      <div v-else class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
        <div v-for="reporte in reportes" :key="reporte.id"
          class="bg-white rounded-2xl overflow-hidden shadow-xl text-gray-800">

          <!-- Header tarjeta -->
          <div class="p-5 border-b border-gray-100">
            <div class="flex items-start gap-3">
              <div class="text-3xl">{{ iconTipo(reporte.tipo) }}</div>
              <div class="flex-1">
                <h3 class="font-black text-sm leading-tight">{{ reporte.tipo_display }}</h3>
                <p class="text-gray-400 text-xs mt-1">
                  📅 Generado: {{ formatFecha(reporte.fecha) }} &nbsp;
                  👤 Por: {{ reporte.generado_por_nombre }}
                </p>
              </div>
            </div>
            <p class="text-gray-600 text-xs mt-3 leading-relaxed">
              {{ descripcionTipo(reporte.tipo) }}
            </p>
          </div>

          <!-- Stats del reporte -->
          <div class="p-5">
            <!-- General -->
            <div v-if="reporte.tipo === 'general'" class="grid grid-cols-3 gap-2 text-center">
              <div>
                <p class="font-black text-xl text-blue-700">{{ reporte.datos.total_respuestas }}</p>
                <p class="text-xs text-gray-400">RESPUESTAS</p>
              </div>
              <div>
                <p class="font-black text-xl text-blue-700">{{ reporte.datos.total_estudiantes }}</p>
                <p class="text-xs text-gray-400">ESTUDIANTES</p>
              </div>
              <div>
                <p class="font-black text-xl text-blue-700">{{ reporte.datos.total_tests }}</p>
                <p class="text-xs text-gray-400">TESTS</p>
              </div>
            </div>

            <!-- Comparativa -->
            <div v-else-if="reporte.tipo === 'comparativa'" class="space-y-2">
              <div v-for="test in reporte.datos.tests" :key="test.test_nombre"
                class="flex justify-between items-center text-sm">
                <span class="text-gray-600 truncate flex-1">{{ test.test_nombre }}</span>
                <span class="font-black text-blue-700 ml-2">
                  {{ Math.max(test.promedio_tiempo, test.promedio_metodos, test.promedio_entorno) }}%
                </span>
              </div>
            </div>

            <!-- Críticas -->
            <div v-else-if="reporte.tipo === 'criticas'" class="grid grid-cols-3 gap-2 text-center">
              <div>
                <p class="font-black text-lg text-blue-700">{{ reporte.datos.promedio_tiempo }}%</p>
                <p class="text-xs text-gray-400">TIEMPO</p>
              </div>
              <div>
                <p class="font-black text-lg text-blue-700">{{ reporte.datos.promedio_metodos }}%</p>
                <p class="text-xs text-gray-400">MÉTODOS</p>
              </div>
              <div>
                <p class="font-black text-lg text-blue-700">{{ reporte.datos.promedio_entorno }}%</p>
                <p class="text-xs text-gray-400">ENTORNO</p>
              </div>
            </div>

            <!-- Tags -->
            <div class="flex gap-2 mt-4 flex-wrap">
              <span v-for="tag in tagsTipo(reporte.tipo)" :key="tag"
                class="px-2 py-1 rounded-full text-xs font-bold"
                :class="tag.color">
                {{ tag.label }}
              </span>
            </div>
          </div>

          <!-- Acciones -->
          <div class="px-5 pb-5 flex gap-2">
            <button @click="verReporte(reporte)"
              class="flex-1 bg-blue-900 hover:bg-blue-800 text-white font-bold py-2
                     rounded-lg text-sm transition-all flex items-center justify-center gap-1">
              👁 Ver Reporte
            </button>
            <button @click="descargarPDF(reporte)"
              class="flex-1 border border-blue-900 text-blue-900 font-bold py-2
                     rounded-lg text-sm hover:bg-blue-50 transition-all
                     flex items-center justify-center gap-1">
              ⬇️ Descargar
            </button>
            <button @click="confirmarEliminar(reporte)"
              class="border border-red-200 text-red-400 font-bold py-2 px-3
                     rounded-lg text-sm hover:bg-red-50 transition-all">
              🗑
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- ═══════════════════════════════════════════════ -->
    <!-- MODAL: Generar nuevo reporte                    -->
    <!-- ═══════════════════════════════════════════════ -->
    <div v-if="modalGenerar"
      class="fixed inset-0 bg-black/70 flex items-center justify-center z-50 px-4"
      @click.self="modalGenerar = false">
      <div class="bg-gray-900 border border-white/20 rounded-2xl p-8 max-w-md w-full">
        <div class="flex justify-between items-center mb-6">
          <h2 class="text-xl font-black">+ Generar Nuevo Reporte</h2>
          <button @click="modalGenerar = false" class="text-white/50 hover:text-white text-xl">✕</button>
        </div>

        <div class="space-y-3 mb-8">
          <button v-for="tipo in tiposReporte" :key="tipo.valor"
            @click="tipoSeleccionado = tipo.valor"
            :class="tipoSeleccionado === tipo.valor
              ? 'border-cyan-400 bg-cyan-400/10'
              : 'border-white/20 hover:border-white/40'"
            class="w-full border rounded-xl p-4 text-left transition-all">
            <div class="flex items-start gap-3">
              <span class="text-2xl">{{ tipo.icono }}</span>
              <div>
                <p class="font-black text-sm">{{ tipo.label }}</p>
                <p class="text-white/50 text-xs mt-1">{{ tipo.descripcion }}</p>
              </div>
            </div>
          </button>
        </div>

        <div class="flex gap-3">
          <button @click="generarReporte" :disabled="!tipoSeleccionado || generando"
            class="flex-1 bg-cyan-500 hover:bg-cyan-400 text-black font-black py-3
                   rounded-full transition-all disabled:opacity-50">
            {{ generando ? 'Generando...' : '✅ Generar' }}
          </button>
          <button @click="modalGenerar = false"
            class="px-6 border border-white/20 text-white font-bold py-3
                   rounded-full hover:bg-white/10 transition-all">
            Cancelar
          </button>
        </div>
      </div>
    </div>

    <!-- ═══════════════════════════════════════════════ -->
    <!-- MODAL: Ver reporte detalle                      -->
    <!-- ═══════════════════════════════════════════════ -->
    <div v-if="reporteDetalle"
      class="fixed inset-0 bg-black/70 flex items-center justify-center z-50 px-4 py-8 overflow-y-auto"
      @click.self="reporteDetalle = null">
      <div class="bg-white text-gray-800 rounded-2xl p-8 max-w-2xl w-full">
        <div class="flex justify-between items-start mb-6">
          <div>
            <h2 class="text-2xl font-black">{{ reporteDetalle.tipo_display }}</h2>
            <p class="text-gray-400 text-sm mt-1">
              Generado el {{ formatFechaCompleta(reporteDetalle.fecha) }}
              por {{ reporteDetalle.generado_por_nombre }}
            </p>
          </div>
          <button @click="reporteDetalle = null" class="text-gray-400 hover:text-gray-600 text-xl">✕</button>
        </div>

        <!-- Detalle General -->
        <div v-if="reporteDetalle.tipo === 'general'">
          <div class="grid grid-cols-3 gap-4 mb-6">
            <div class="bg-blue-50 rounded-xl p-4 text-center">
              <p class="font-black text-3xl text-blue-700">{{ reporteDetalle.datos.total_respuestas }}</p>
              <p class="text-xs text-gray-500 mt-1">TOTAL RESPUESTAS</p>
            </div>
            <div class="bg-blue-50 rounded-xl p-4 text-center">
              <p class="font-black text-3xl text-blue-700">{{ reporteDetalle.datos.total_estudiantes }}</p>
              <p class="text-xs text-gray-500 mt-1">ESTUDIANTES</p>
            </div>
            <div class="bg-blue-50 rounded-xl p-4 text-center">
              <p class="font-black text-3xl text-blue-700">{{ reporteDetalle.datos.total_tests }}</p>
              <p class="text-xs text-gray-500 mt-1">TESTS ACTIVOS</p>
            </div>
          </div>
          <h3 class="font-black mb-3">PROMEDIO DE DEBILIDAD POR ÁREA</h3>
          <div class="space-y-3">
            <div v-for="area in [
              { label: 'Gestión del Tiempo', valor: reporteDetalle.datos.promedio_tiempo, color: 'bg-cyan-400' },
              { label: 'Métodos de Estudio', valor: reporteDetalle.datos.promedio_metodos, color: 'bg-blue-500' },
              { label: 'Entorno Personal', valor: reporteDetalle.datos.promedio_entorno, color: 'bg-indigo-500' },
            ]" :key="area.label">
              <div class="flex justify-between text-sm mb-1">
                <span>{{ area.label }}</span>
                <span class="font-black">{{ area.valor }}%</span>
              </div>
              <div class="w-full bg-gray-100 rounded-full h-3">
                <div :class="area.color" class="h-3 rounded-full transition-all"
                  :style="`width: ${area.valor}%`" />
              </div>
            </div>
          </div>
        </div>

        <!-- Detalle Comparativa -->
        <div v-else-if="reporteDetalle.tipo === 'comparativa'">
          <div v-for="test in reporteDetalle.datos.tests" :key="test.test_nombre"
            class="mb-6 p-4 bg-gray-50 rounded-xl">
            <h3 class="font-black mb-3">{{ test.test_nombre }}</h3>
            <div class="grid grid-cols-3 gap-3 text-center">
              <div>
                <p class="font-black text-xl text-cyan-600">{{ test.promedio_tiempo }}%</p>
                <p class="text-xs text-gray-400">TIEMPO</p>
              </div>
              <div>
                <p class="font-black text-xl text-blue-600">{{ test.promedio_metodos }}%</p>
                <p class="text-xs text-gray-400">MÉTODOS</p>
              </div>
              <div>
                <p class="font-black text-xl text-indigo-600">{{ test.promedio_entorno }}%</p>
                <p class="text-xs text-gray-400">ENTORNO</p>
              </div>
            </div>
            <p class="text-xs text-gray-400 mt-2 text-right">
              {{ test.total_respuestas }} respuestas
            </p>
          </div>
        </div>

        <!-- Detalle Críticas -->
        <div v-else-if="reporteDetalle.tipo === 'criticas'">
          <div class="bg-red-50 border border-red-200 rounded-xl p-4 mb-6">
            <p class="font-black text-red-700">⚠️ Área más crítica: {{ reporteDetalle.datos.area_critica }}</p>
            <p class="text-sm text-gray-500 mt-1">
              Basado en {{ reporteDetalle.datos.total_analizados }} evaluaciones
            </p>
          </div>
          <div class="space-y-3">
            <div v-for="area in [
              { label: 'Gestión del Tiempo', valor: reporteDetalle.datos.promedio_tiempo, color: 'bg-cyan-400' },
              { label: 'Métodos de Estudio', valor: reporteDetalle.datos.promedio_metodos, color: 'bg-blue-500' },
              { label: 'Entorno Personal', valor: reporteDetalle.datos.promedio_entorno, color: 'bg-indigo-500' },
            ]" :key="area.label">
              <div class="flex justify-between text-sm mb-1">
                <span>{{ area.label }}</span>
                <span class="font-black">{{ area.valor }}%</span>
              </div>
              <div class="w-full bg-gray-100 rounded-full h-3">
                <div :class="area.color" class="h-3 rounded-full"
                  :style="`width: ${area.valor}%`" />
              </div>
            </div>
          </div>
        </div>

        <div class="flex gap-3 mt-8">
          <button @click="descargarPDF(reporteDetalle)"
            class="flex-1 bg-blue-900 hover:bg-blue-800 text-white font-black py-3
                   rounded-full transition-all">
            ⬇️ Descargar PDF
          </button>
          <button @click="reporteDetalle = null"
            class="px-6 border border-gray-200 text-gray-600 font-bold py-3
                   rounded-full hover:bg-gray-50 transition-all">
            Cerrar
          </button>
        </div>
      </div>
    </div>

    <!-- Modal confirmar eliminar -->
    <div v-if="reporteAEliminar"
      class="fixed inset-0 bg-black/70 flex items-center justify-center z-50 px-4">
      <div class="bg-gray-900 border border-red-500/40 rounded-2xl p-8 max-w-sm w-full">
        <h3 class="text-xl font-black mb-3">¿Eliminar reporte?</h3>
        <p class="text-white/70 mb-6">Esta acción no se puede deshacer.</p>
        <div class="flex gap-3">
          <button @click="eliminarReporte"
            class="flex-1 bg-red-600 hover:bg-red-500 text-white font-black py-3 rounded-full">
            Eliminar
          </button>
          <button @click="reporteAEliminar = null"
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
import NavBar from '../components/NavBar.vue'
import api from '../api/axios'
import jsPDF from 'jspdf'
import autoTable from 'jspdf-autotable'

const reportes = ref([])
const loading = ref(true)
const modalGenerar = ref(false)
const tipoSeleccionado = ref('')
const generando = ref(false)
const reporteDetalle = ref(null)
const reporteAEliminar = ref(null)

const tiposReporte = [
  {
    valor: 'general',
    icono: '📊',
    label: 'Análisis General de Hábitos',
    descripcion: 'Resumen global: respuestas, estudiantes, promedios por área.'
  },
  {
    valor: 'comparativa',
    icono: '⚖️',
    label: 'Comparativa por Test',
    descripcion: 'Compara el rendimiento promedio entre los tests aplicados.'
  },
  {
    valor: 'criticas',
    icono: '🎯',
    label: 'Áreas Críticas de Atención',
    descripcion: 'Identifica las áreas con mayor debilidad entre los estudiantes.'
  },
]

onMounted(async () => {
  try {
    const { data } = await api.get('/reportes/')
    reportes.value = data
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
})

async function generarReporte() {
  generando.value = true
  try {
    const { data } = await api.post('/reportes/generar/', { tipo: tipoSeleccionado.value })
    reportes.value.unshift(data)
    modalGenerar.value = false
    tipoSeleccionado.value = ''
  } catch (e) {
    console.error(e)
  } finally {
    generando.value = false
  }
}

function verReporte(reporte) {
  reporteDetalle.value = reporte
}

function confirmarEliminar(reporte) {
  reporteAEliminar.value = reporte
}

async function eliminarReporte() {
  try {
    await api.delete(`/reportes/${reporteAEliminar.value.uuid}/`)
    reportes.value = reportes.value.filter(r => r.uuid !== reporteAEliminar.value.uuid)
    reporteAEliminar.value = null
  } catch (e) {
    console.error(e)
  }
}

function descargarPDF(reporte) {
  const doc = new jsPDF()
  const fecha = formatFechaCompleta(reporte.fecha)

  // Header
  doc.setFillColor(13, 42, 92)
  doc.rect(0, 0, 210, 35, 'F')
  doc.setTextColor(255, 255, 255)
  doc.setFontSize(18)
  doc.setFont('helvetica', 'bold')
  doc.text('RECONOCE Y MEJORA TUS HÁBITOS DE ESTUDIO', 105, 15, { align: 'center' })
  doc.setFontSize(12)
  doc.text(reporte.tipo_display.toUpperCase(), 105, 25, { align: 'center' })

  // Info generación
  doc.setTextColor(100, 100, 100)
  doc.setFontSize(9)
  doc.setFont('helvetica', 'normal')
  doc.text(`Generado: ${fecha}  |  Por: ${reporte.generado_por_nombre}`, 14, 43)

  doc.setDrawColor(200, 200, 200)
  doc.line(14, 46, 196, 46)

  let y = 55

  if (reporte.tipo === 'general') {
    const d = reporte.datos

    doc.setTextColor(13, 42, 92)
    doc.setFontSize(13)
    doc.setFont('helvetica', 'bold')
    doc.text('RESUMEN GENERAL', 14, y)
    y += 8

    autoTable(doc, {
      startY: y,
      head: [['Métrica', 'Valor']],
      body: [
        ['Total de Respuestas', d.total_respuestas],
        ['Total de Estudiantes', d.total_estudiantes],
        ['Tests Activos', d.total_tests],
      ],
      styles: { fontSize: 10 },
      headStyles: { fillColor: [13, 42, 92] },
    })

    y = doc.lastAutoTable.finalY + 10

    doc.setFontSize(13)
    doc.setFont('helvetica', 'bold')
    doc.setTextColor(13, 42, 92)
    doc.text('PROMEDIO DE DEBILIDAD POR ÁREA', 14, y)
    y += 8

    autoTable(doc, {
      startY: y,
      head: [['Área', 'Promedio de Debilidad', 'Nivel']],
      body: [
        ['Gestión del Tiempo', `${d.promedio_tiempo}%`, nivelTexto(d.promedio_tiempo)],
        ['Métodos de Estudio', `${d.promedio_metodos}%`, nivelTexto(d.promedio_metodos)],
        ['Entorno Personal', `${d.promedio_entorno}%`, nivelTexto(d.promedio_entorno)],
      ],
      styles: { fontSize: 10 },
      headStyles: { fillColor: [13, 42, 92] },
    })

  } else if (reporte.tipo === 'comparativa') {
    doc.setTextColor(13, 42, 92)
    doc.setFontSize(13)
    doc.setFont('helvetica', 'bold')
    doc.text('COMPARATIVA POR TEST', 14, y)
    y += 8

    const rows = reporte.datos.tests.map(t => [
      t.test_nombre,
      `${t.promedio_tiempo}%`,
      `${t.promedio_metodos}%`,
      `${t.promedio_entorno}%`,
      t.total_respuestas,
    ])

    autoTable(doc, {
      startY: y,
      head: [['Test', 'Tiempo', 'Métodos', 'Entorno', 'Respuestas']],
      body: rows,
      styles: { fontSize: 10 },
      headStyles: { fillColor: [13, 42, 92] },
    })

  } else if (reporte.tipo === 'criticas') {
    const d = reporte.datos

    doc.setTextColor(13, 42, 92)
    doc.setFontSize(13)
    doc.setFont('helvetica', 'bold')
    doc.text('ÁREAS CRÍTICAS DE ATENCIÓN', 14, y)
    y += 8

    autoTable(doc, {
      startY: y,
      head: [['Área', 'Promedio Debilidad', 'Estado']],
      body: [
        ['Gestión del Tiempo', `${d.promedio_tiempo}%`, nivelTexto(d.promedio_tiempo)],
        ['Métodos de Estudio', `${d.promedio_metodos}%`, nivelTexto(d.promedio_metodos)],
        ['Entorno Personal', `${d.promedio_entorno}%`, nivelTexto(d.promedio_entorno)],
      ],
      styles: { fontSize: 10 },
      headStyles: { fillColor: [13, 42, 92] },
    })

    y = doc.lastAutoTable.finalY + 10
    doc.setFontSize(11)
    doc.setTextColor(180, 0, 0)
    doc.setFont('helvetica', 'bold')
    doc.text(`⚠ Área más crítica: ${d.area_critica}`, 14, y)
    y += 6
    doc.setTextColor(100, 100, 100)
    doc.setFont('helvetica', 'normal')
    doc.setFontSize(9)
    doc.text(`Basado en ${d.total_analizados} evaluaciones realizadas.`, 14, y)
  }

  // Footer
  const pageH = doc.internal.pageSize.height
  doc.setDrawColor(200, 200, 200)
  doc.line(14, pageH - 15, 196, pageH - 15)
  doc.setFontSize(8)
  doc.setTextColor(150, 150, 150)
  doc.text('Reconoce y Mejora Tus Hábitos de Estudio  ·  Reporte generado automáticamente', 105, pageH - 8, { align: 'center' })

  doc.save(`reporte_${reporte.tipo}_${new Date().toISOString().slice(0,10)}.pdf`)
}

// Helpers
function nivelTexto(valor) {
  if (valor >= 65) return '🔴 Alto'
  if (valor >= 40) return '🟡 Medio'
  return '🟢 Bajo'
}

function iconTipo(tipo) {
  return { general: '📊', comparativa: '⚖️', criticas: '🎯' }[tipo] || '📋'
}

function descripcionTipo(tipo) {
  return {
    general: 'Reporte completo sobre tendencias generales en hábitos de estudio de todos los estudiantes.',
    comparativa: 'Comparación detallada del rendimiento entre los tests aplicados.',
    criticas: 'Identificación de las áreas con mayor porcentaje de debilidad entre los estudiantes.',
  }[tipo] || ''
}

function tagsTipo(tipo) {
  const ahora = new Date()
  const mes = ahora.toLocaleString('es-MX', { month: 'long' })  
  const año = ahora.getFullYear()
  const base = { label: `${mes.charAt(0).toUpperCase() + mes.slice(1)} ${año}`, color: 'bg-blue-100 text-blue-700' }
  const tags = {
    general: [
      { label: 'Todos los tests', color: 'bg-cyan-100 text-cyan-700' },
      { label: 'Todas las áreas', color: 'bg-yellow-100 text-yellow-700' },
    ],
    comparativa: [
      { label: 'Comparativa', color: 'bg-yellow-100 text-yellow-700' },
    ],
    criticas: [
      { label: 'Todos los tests', color: 'bg-cyan-100 text-cyan-700' },
      { label: 'Áreas críticas', color: 'bg-yellow-100 text-yellow-700' },
    ],
  }
  return [...(tags[tipo] || []), base]
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
