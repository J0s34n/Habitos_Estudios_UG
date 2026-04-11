<template>
  <div class="min-h-screen flex items-center justify-center px-4">
    <div class="w-full max-w-2xl">
      <div class="flex justify-between items-center mb-8">
        <h1 class="text-3xl font-black text-white">QUEJAS O SUGERENCIA</h1>
        <RouterLink :to="auth.isLoggedIn ? '/menu' : '/'" class="text-blue-300 hover:text-white transition-all text-sm">← Volver</RouterLink>
      </div>

      <div class="bg-white rounded-2xl p-8">
        <!-- Tipo -->
        <div class="mb-6">
          <p class="font-black text-center mb-4 tracking-widest text-sm text-gray-800">SELECCIONA UNO</p>
          <div class="flex gap-4 justify-center">
            <button @click="form.tipo = 'queja'"
              :class="form.tipo === 'queja'
                ? 'bg-blue-900 text-white ring-2 ring-blue-400'
                : 'bg-blue-900/80 text-white hover:bg-blue-800'"
              class="px-8 py-3 rounded-lg font-bold transition-all">
              QUEJA
            </button>
            <button @click="form.tipo = 'sugerencia'"
              :class="form.tipo === 'sugerencia'
                ? 'bg-blue-900 text-white ring-2 ring-blue-400'
                : 'bg-blue-900/80 text-white hover:bg-blue-800'"
              class="px-8 py-3 rounded-lg font-bold transition-all">
              SUGERENCIA
            </button>
          </div>
        </div>

        <!-- Comentarios -->
        <div class="mb-6">
          <label class="block font-bold mb-2 text-sm tracking-widest text-gray-700">COMENTARIOS:</label>
        <input v-model="form.comentario" type="text"
          class="w-full border border-gray-300 rounded-lg py-3 px-4
                focus:outline-none focus:border-blue-500 bg-gray-100 text-gray-800
                placeholder-gray-400" 
          placeholder="Escribe tu comentario aquí..." />
        </div>

        <!-- Email -->
        <div class="mb-8">
          <label class="block font-bold mb-2 text-sm tracking-widest text-gray-700">EMAIL:</label>
          <input v-model="form.email" type="email"
          class="w-full border border-gray-300 rounded-lg py-3 px-4
                focus:outline-none focus:border-blue-500 bg-gray-100 text-gray-800
                placeholder-gray-400"
          placeholder="tu@email.com" />
        </div>

        <div class="text-center">
          <button @click="enviar" :disabled="loading || enviado"
            class="bg-blue-900 text-white font-bold py-3 px-12 rounded-lg
                   hover:bg-blue-800 transition-all disabled:opacity-50">
            {{ enviado ? '¡ENVIADO! ✓' : loading ? 'ENVIANDO...' : 'ENVIAR' }}
          </button>
          <p v-if="error" class="text-red-500 text-sm mt-3">{{ error }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import api from '../api/axios'

const form = ref({ tipo: 'queja', comentario: '', email: '' })
const loading = ref(false)
const enviado = ref(false)
const error = ref('')
const auth = useAuthStore()

async function enviar() {
  if (!form.value.comentario || !form.value.email) {
    error.value = 'Por favor completa todos los campos'
    return
  }
  error.value = ''
  loading.value = true
  try {
    await api.post('/usuarios/buzon/', form.value)
    enviado.value = true
  } catch {
    error.value = 'Error al enviar. Intenta de nuevo.'
  } finally {
    loading.value = false
  }
}
</script>