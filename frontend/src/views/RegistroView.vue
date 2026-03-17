<template>
  <div class="min-h-screen flex items-center justify-center px-4 py-8">
    <div class="w-full max-w-4xl flex flex-col md:flex-row items-center gap-8">

      <!-- Título — oculto en móvil -->
      <div class="hidden md:block flex-1">
        <h1 class="text-6xl font-black text-white leading-tight">REGISTRO</h1>
      </div>

      <!-- Formulario -->
      <div class="w-full md:flex-1">
        <!-- Título móvil -->
        <h1 class="md:hidden text-4xl font-black text-white text-center mb-6">
          REGISTRO
        </h1>

        <div class="flex justify-end mb-4">
          <RouterLink to="/login"
            class="border border-white text-white px-6 py-2 rounded-full
                   hover:bg-white hover:text-blue-900 transition-all text-sm">
            INICIO DE SESIÓN
          </RouterLink>
        </div>

        <div class="bg-blue-900/60 border border-blue-400/20 rounded-2xl overflow-hidden">
          <!-- Nombre y primer apellido -->
          <div class="p-5 border-b border-blue-400/30 grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label class="block text-white text-xs mb-2 tracking-widest">NOMBRE</label>
              <input v-model="form.first_name" type="text"
                class="w-full bg-transparent border border-white/30 rounded-full py-2 px-4
                       text-white focus:outline-none focus:border-white text-sm" />
            </div>
            <div>
              <label class="block text-white text-xs mb-2 tracking-widest">PRIMER APELLIDO</label>
              <input v-model="form.primer_apellido" type="text"
                class="w-full bg-transparent border border-white/30 rounded-full py-2 px-4
                       text-white focus:outline-none focus:border-white text-sm" />
            </div>
          </div>

          <!-- Segundo apellido y email -->
          <div class="p-5 border-b border-blue-400/30 grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label class="block text-white text-xs mb-2 tracking-widest">SEGUNDO APELLIDO</label>
              <input v-model="form.segundo_apellido" type="text"
                class="w-full bg-transparent border border-white/30 rounded-full py-2 px-4
                       text-white focus:outline-none focus:border-white text-sm" />
            </div>
            <div>
              <label class="block text-white text-xs mb-2 tracking-widest">EMAIL</label>
              <input v-model="form.email" type="email"
                class="w-full bg-transparent border border-white/30 rounded-full py-2 px-4
                       text-white focus:outline-none focus:border-white text-sm" />
            </div>
          </div>

          <!-- Usuario -->
          <div class="p-5 border-b border-blue-400/30">
            <label class="block text-white text-xs mb-2 tracking-widest">USUARIO</label>
            <input v-model="form.username" type="text"
              class="w-full bg-transparent border border-white/30 rounded-full py-2 px-4
                     text-white focus:outline-none focus:border-white text-sm" />
          </div>

          <!-- Contraseña -->
          <div class="p-5 border-b border-blue-400/30">
            <label class="block text-white text-xs mb-2 tracking-widest">CONTRASEÑA</label>
            <input v-model="form.password" type="password"
              class="w-full bg-transparent border border-white/30 rounded-full py-2 px-4
                     text-white focus:outline-none focus:border-white text-sm" />
          </div>

          <div class="p-5">
            <button @click="handleRegistro" :disabled="loading"
              class="w-full bg-black text-white py-3 rounded-full font-bold
                     hover:bg-gray-800 transition-all disabled:opacity-50">
              {{ loading ? 'REGISTRANDO...' : 'REGISTRAR' }}
            </button>
            <p v-if="error" class="text-red-400 text-sm mt-3 text-center">{{ error }}</p>
            <p v-if="exito" class="text-green-400 text-sm mt-3 text-center">
              ¡Cuenta creada!
              <RouterLink to="/login" class="underline">Inicia sesión</RouterLink>
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '../stores/auth'

const auth = useAuthStore()
const loading = ref(false)
const error = ref('')
const exito = ref(false)

const form = ref({
  username: '',
  first_name: '',
  primer_apellido: '',
  segundo_apellido: '',
  email: '',
  password: ''
})

async function handleRegistro() {
  error.value = ''
  exito.value = false
  loading.value = true
  try {
    await auth.registro(form.value)
    exito.value = true
  } catch (e) {
    error.value = e.response?.data
      ? Object.values(e.response.data).flat().join(' ')
      : 'Error al registrarse'
  } finally {
    loading.value = false
  }
}
</script>