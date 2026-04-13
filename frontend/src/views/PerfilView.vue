<template>
  <div class="min-h-screen text-white">
    <NavBar />
    <div class="w-full px-4 sm:px-6 lg:px-10 pb-8 flex items-center justify-center min-h-[80vh]">
      <div class="w-full max-w-3xl flex flex-col md:flex-row items-center gap-8">

        <!-- Ícono izquierda -->
        <div class="hidden md:flex flex-col items-center gap-4">
          <h1 class="text-4xl font-black text-white text-center">INFORMACION<br>PERSONAL</h1>
          <div class="text-9xl">👤</div>
        </div>

        <!-- Título móvil -->
        <h1 class="md:hidden text-3xl font-black text-white text-center">
          INFORMACION PERSONAL
        </h1>

        <!-- Formulario -->
        <div class="flex-1 w-full">
          <div class="bg-white rounded-2xl p-8 shadow-xl">
            <div class="space-y-5">
              <div>
                <label class="block font-black text-sm mb-2 tracking-widest text-gray-700">NOMBRE:</label>
                <input v-model="form.first_name" type="text"
                  class="w-full border border-gray-300 rounded-lg py-3 px-4
                         focus:outline-none focus:border-blue-500 bg-gray-100 text-gray-800" />
              </div>
              <div>
                <label class="block font-black text-sm mb-2 tracking-widest text-gray-700">APELLIDOS:</label>
                <input v-model="form.apellidos" type="text"
                  class="w-full border border-gray-300 rounded-lg py-3 px-4
                         focus:outline-none focus:border-blue-500 bg-gray-100 text-gray-800" />
              </div>
              <div>
                <label class="block font-black text-sm mb-2 tracking-widest text-gray-700">EMAIL:</label>
                <input v-model="form.email" type="email"
                  class="w-full border border-gray-300 rounded-lg py-3 px-4
                         focus:outline-none focus:border-blue-500 bg-gray-100 text-gray-800" />
              </div>
              <div>
                <label class="block font-black text-sm mb-2 tracking-widest text-gray-700">CONTRASEÑA:</label>
                <input v-model="form.password" type="password"
                  placeholder="Dejar vacío para no cambiar"
                  class="w-full border border-gray-300 rounded-lg py-3 px-4
                         focus:outline-none focus:border-blue-500 bg-gray-100 text-gray-800
                         placeholder-gray-400" />
              </div>

              <div class="flex gap-3 pt-2">
                <button @click="guardar" :disabled="loading"
                  class="flex-1 bg-blue-900 text-white font-bold py-3 rounded-lg
                         hover:bg-blue-800 transition-all disabled:opacity-50">
                  {{ loading ? 'GUARDANDO...' : 'ENVIAR' }}
                </button>
                <RouterLink to="/menu"
                  class="flex-1 border border-gray-300 text-gray-600 font-bold py-3 rounded-lg
                         text-center hover:bg-gray-50 transition-all">
                  CANCELAR
                </RouterLink>
              </div>

              <p v-if="exito" class="text-green-600 text-sm text-center font-semibold">
                ✓ Perfil actualizado correctamente
              </p>
              <p v-if="error" class="text-red-500 text-sm text-center">{{ error }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import api from '../api/axios'
import NavBar from '@/components/NavBar.vue'

const auth = useAuthStore()
const loading = ref(false)
const exito = ref(false)
const error = ref('')

const form = ref({
  first_name: '',
  apellidos: '',
  email: '',
  password: ''
})

onMounted(() => {
  if (auth.user) {
    form.value.first_name = auth.user.first_name || ''
    form.value.apellidos = `${auth.user.primer_apellido || ''} ${auth.user.segundo_apellido || ''}`.trim()
    form.value.email = auth.user.email || ''
  }
})

async function guardar() {
  error.value = ''
  exito.value = false
  loading.value = true
  try {
    const payload = {
      first_name: form.value.first_name,
      email: form.value.email,
    }
    if (form.value.password) payload.password = form.value.password

    await api.patch('/usuarios/perfil/', payload)
    await auth.fetchPerfil()
    exito.value = true
  } catch (e) {
    error.value = 'Error al actualizar. Verifica los datos.'
  } finally {
    loading.value = false
  }
}
</script>