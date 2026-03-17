<template>
  <div class="min-h-screen text-white">
    <NavBar />
    <div class="w-full px-4 sm:px-6 lg:px-10 pb-8">

      <!-- Saludo -->
      <div class="mb-6">
        <p class="text-xl">Hola: <strong>{{ auth.user?.first_name || auth.user?.username }}</strong></p>
        <p class="text-blue-300">Bienvenido</p>
      </div>

      <!-- Grid responsivo -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 w-full">

        <!-- Iniciar nuevo test -->
        <RouterLink to="/test/1"
          class="bg-amber-700/60 rounded-2xl p-6 hover:bg-amber-600/70 transition-all
                 flex flex-col items-start justify-between min-h-40 border border-amber-500/30
                 sm:row-span-2">
          <div class="text-right w-full text-2xl">›</div>
          <div>
            <div class="text-4xl mb-3">📋</div>
            <p class="font-black text-lg">INICIAR UN<br>NUEVO TEST</p>
          </div>
        </RouterLink>

        <!-- Evaluaciones pasadas -->
        <RouterLink to="/evaluaciones"
          class="bg-amber-700/60 rounded-2xl p-5 hover:bg-amber-600/70 transition-all
                 flex justify-between items-center border border-amber-500/30">
          <div>
            <div class="text-2xl mb-1">🕐</div>
            <p class="font-black text-sm sm:text-base">EVALUACIONES<br>PASADAS</p>
          </div>
          <span class="text-2xl flex-shrink-0">›</span>
        </RouterLink>

        <!-- Información personal -->
        <RouterLink to="/perfil"
          class="bg-amber-700/60 rounded-2xl p-6 hover:bg-amber-600/70 transition-all
                 flex flex-col items-center justify-between border border-amber-500/30
                 row-span-1 sm:row-span-2">
          <p class="font-black text-lg text-center">INFORMACIÓN<br>PERSONAL</p>
          <div class="text-6xl">👤</div>
          <span class="text-2xl self-end">›</span>
        </RouterLink>

        <!-- Quejas -->
        <RouterLink to="/buzon"
          class="bg-amber-700/60 rounded-2xl p-5 hover:bg-amber-600/70 transition-all
                 flex justify-between items-center border border-amber-500/30">
          <div>
            <div class="text-2xl mb-1">📬</div>
            <p class="font-black text-sm sm:text-base">QUEJAS<br>O SUGERENCIAS</p>
          </div>
          <span class="text-2xl flex-shrink-0">›</span>
        </RouterLink>

      </div>
    </div>
  </div>
</template>

<script setup>
import NavBar from '../components/NavBar.vue'
import { useAuthStore } from '../stores/auth'
const auth = useAuthStore()
</script>
