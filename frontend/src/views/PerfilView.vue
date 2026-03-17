<template>
  <div class="min-h-screen flex items-center justify-center px-4">
    <div class="w-full max-w-3xl flex items-center gap-12">
      <NavBar />
      <!-- Ícono izquierda -->
      <div class="hidden md:flex flex-col items-center gap-4">
        <h1 class="text-4xl font-black text-white">INFORMACION<br>PERSONAL</h1>
        <div class="text-9xl">👤</div>
      </div>

      <!-- Formulario derecha -->
      <div class="flex-1">
        <div class="bg-white rounded-2xl p-8 shadow-xl">
          <div class="space-y-5">
            <div>
              <label class="block font-black text-sm mb-2 tracking-widest">NOMBRE:</label>
              <input v-model="form.first_name" type="text"
                class="w-full border border-gray-300 rounded-lg py-3 px-4
                       focus:outline-none focus:border-blue-500 bg-gray-100" />
            </div>
            <div>
              <label class="block font-black text-sm mb-2 tracking-widest">APELLIDOS:</label>
              <input v-model="form.apellidos" type="text"
                class="w-full border border-gray-300 rounded-lg py-3 px-4
                       focus:outline-none focus:border-blue-500 bg-gray-100" />
            </div>
            <div>
              <label class="block font-black text-sm mb-2 tracking-widest">EMAIL:</label>
              <input v-model="form.email" type="email"
                class="w-full border border-gray-300 rounded-lg py-3 px-4
                       focus:outline-none focus:border-blue-500 bg-gray-100" />
            </div>
            <div>
              <label class="block font-black text-sm mb-2 tracking-widest">CONTRASEÑA:</label>
              <input v-model="form.password" type="password" placeholder="Dejar vacío para no cambiar"
                class="w-full border border-gray-300 rounded-lg py-3 px-4
                       focus:outline-none focus:border-blue-500 bg-gray-100" />
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