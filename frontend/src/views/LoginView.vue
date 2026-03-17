<template>
  <div class="min-h-screen flex items-center justify-center px-4 py-8">
    <div class="w-full max-w-4xl flex flex-col md:flex-row items-center gap-8">

      <!-- Título — oculto en móvil, visible en md+ -->
      <div class="hidden md:block flex-1">
        <h1 class="text-6xl font-black text-white leading-tight">
          INICIO DE<br>SESIÓN
        </h1>
      </div>

      <!-- Formulario -->
      <div class="w-full md:flex-1">
        <!-- Título móvil -->
        <h1 class="md:hidden text-4xl font-black text-white text-center mb-6">
          INICIO DE SESIÓN
        </h1>

        <div class="flex justify-end mb-4">
          <RouterLink to="/registro"
            class="border border-white text-white px-6 py-2 rounded-full
                   hover:bg-white hover:text-blue-900 transition-all text-sm">
            REGISTRARSE
          </RouterLink>
        </div>

        <div class="bg-blue-900/60 border border-blue-400/20 rounded-2xl overflow-hidden">
          <div class="p-5 border-b border-blue-400/30">
            <label class="block text-white text-xs mb-2 tracking-widest">USUARIO</label>
            <input v-model="form.username" type="text"
              class="w-full bg-transparent border border-white/30 rounded-full py-2 px-4
                     text-white placeholder-blue-300 focus:outline-none focus:border-white text-sm" />
          </div>
          <div class="p-5 border-b border-blue-400/30">
            <label class="block text-white text-xs mb-2 tracking-widest">CONTRASEÑA</label>
            <input v-model="form.password" type="password"
              class="w-full bg-transparent border border-white/30 rounded-full py-2 px-4
                     text-white placeholder-blue-300 focus:outline-none focus:border-white text-sm" />
          </div>
          <div class="p-5">
            <button @click="handleLogin" :disabled="loading"
              class="w-full bg-black text-white py-3 rounded-full font-bold
                     hover:bg-gray-800 transition-all disabled:opacity-50">
              {{ loading ? 'CARGANDO...' : 'INICIAR' }}
            </button>
            <p v-if="error" class="text-red-400 text-sm mt-3 text-center">{{ error }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const auth = useAuthStore()
const router = useRouter()
const form = ref({ username: '', password: '' })
const loading = ref(false)
const error = ref('')

async function handleLogin() {
  error.value = ''
  loading.value = true
  try {
    await auth.login(form.value.username, form.value.password)
    router.push(auth.isAdmin ? '/admin' : '/menu')
  } catch {
    error.value = 'Usuario o contraseña incorrectos'
  } finally {
    loading.value = false
  }
}
</script>