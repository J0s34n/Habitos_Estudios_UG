<template>
  <nav class="w-full flex justify-between items-center px-4 sm:px-6 lg:px-12 py-4 border-b border-white/10 mb-6">
    <!-- Saludo -->
    <div class="flex items-center gap-3">
      <RouterLink :to="auth.isAdmin ? '/admin' : '/menu'" 
        class="text-white/50 hover:text-white transition-all text-lg">🏠</RouterLink>
      <RouterLink :to="auth.isAdmin ? '/admin' : '/menu'">
        <p class="text-white font-semibold leading-tight hover:text-blue-300 transition-all">
          {{ auth.user?.first_name || auth.user?.username }}
        </p>
        <p class="text-blue-300 text-xs">
          {{ auth.isAdmin ? 'Administrador' : 'Estudiante' }}
        </p>
      </RouterLink>
    </div>

    <!-- Centro: navegación — oculto en móvil, visible en md+ -->
    <div v-if="!auth.isAdmin" class="hidden md:flex gap-2">
      <RouterLink to="/menu" class="nav-link" :class="esActiva('/menu') ? 'nav-activo' : 'nav-inactivo'">Menú</RouterLink>
      <RouterLink to="/test/1" class="nav-link" :class="esActiva('/test') ? 'nav-activo' : 'nav-inactivo'">Nuevo Test</RouterLink>
      <RouterLink to="/evaluaciones" class="nav-link" :class="esActiva('/evaluaciones') ? 'nav-activo' : 'nav-inactivo'">Evaluaciones</RouterLink>
      <RouterLink to="/perfil" class="nav-link" :class="esActiva('/perfil') ? 'nav-activo' : 'nav-inactivo'">Perfil</RouterLink>
    </div>

    <div v-else class="hidden md:flex gap-2">
      <RouterLink to="/admin" class="nav-link" :class="ruta === '/admin' ? 'nav-activo' : 'nav-inactivo'">Dashboard</RouterLink>
      <RouterLink to="/admin/tests" class="nav-link" :class="esActiva('/admin/tests') ? 'nav-activo' : 'nav-inactivo'">Tests</RouterLink>
      <RouterLink to="/admin/quejas" class="nav-link" :class="esActiva('/admin/quejas') ? 'nav-activo' : 'nav-inactivo'">Quejas</RouterLink>
      <RouterLink to="/admin/reportes" class="nav-link" :class="esActiva('/admin/reportes') ? 'nav-activo' : 'nav-inactivo'">Reportes</RouterLink>
      <RouterLink to="/admin/estudiantes" class="nav-link" :class="esActiva('/admin/estudiantes') ? 'nav-activo' : 'nav-inactivo'">Estudiantes</RouterLink>
      <RouterLink to="/admin/respuestas" class="nav-link" :class="esActiva('/admin/respuestas') ? 'nav-activo' : 'nav-inactivo'">Respuestas</RouterLink>
    </div>

    <!-- Derecha: menú hamburguesa móvil + cerrar sesión -->
    <div class="flex items-center gap-2">
      <!-- Hamburguesa solo en móvil -->
      <button @click="menuMovil = !menuMovil"
        class="md:hidden border border-white/30 text-white px-3 py-2 rounded-full text-sm">
        ☰
      </button>
      <button @click="cerrarSesion"
        class="border border-white/30 text-white/70 px-4 py-2 rounded-full text-sm
               hover:border-red-400 hover:text-red-400 transition-all flex items-center gap-2">
        <span class="hidden sm:inline">Cerrar sesión</span>
        <span>⎋</span>
      </button>
    </div>
  </nav>

  <!-- Menú móvil desplegable -->
  <div v-if="menuMovil" class="md:hidden bg-blue-950/95 border-b border-white/10 px-4 py-3 flex flex-col gap-2">
    <template v-if="!auth.isAdmin">
      <RouterLink to="/menu" @click="menuMovil = false" class="nav-link-movil">🏠 Menú</RouterLink>
      <RouterLink to="/test/1" @click="menuMovil = false" class="nav-link-movil">📝 Nuevo Test</RouterLink>
      <RouterLink to="/evaluaciones" @click="menuMovil = false" class="nav-link-movil">🕐 Evaluaciones</RouterLink>
      <RouterLink to="/perfil" @click="menuMovil = false" class="nav-link-movil">👤 Perfil</RouterLink>
    </template>
    <template v-else>
      <RouterLink to="/admin" @click="menuMovil = false" class="nav-link-movil">📊 Dashboard</RouterLink>
      <RouterLink to="/admin/tests" @click="menuMovil = false" class="nav-link-movil">📝 Tests</RouterLink>
      <RouterLink to="/admin/quejas" @click="menuMovil = false" class="nav-link-movil">📬 Quejas</RouterLink>
      <RouterLink to="/admin/reportes" @click="menuMovil = false" class="nav-link-movil">📈 Reportes</RouterLink>
      <RouterLink to="/admin/estudiantes" @click="menuMovil = false" class="nav-link-movil">👥 Estudiantes</RouterLink>
      <RouterLink to="/admin/respuestas" @click="menuMovil = false" class="nav-link-movil">📋 Respuestas</RouterLink>
    </template>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const auth = useAuthStore()
const router = useRouter()
const route = useRoute()
const menuMovil = ref(false)
const ruta = route.path

function cerrarSesion() {
  auth.logout()
  router.push('/')
}

function esActiva(path) {
  return route.path.startsWith(path)
}
</script>

<style scoped>
.nav-link {
  @apply px-4 py-2 rounded-full text-sm transition-all;
}
.nav-activo {
  @apply bg-white text-blue-900 font-bold;
}
.nav-inactivo {
  @apply text-white/70 hover:text-white hover:bg-white/10;
}
.nav-link-movil {
  @apply block px-4 py-3 text-white/80 hover:text-white hover:bg-white/10 rounded-xl transition-all text-sm font-semibold;
}
</style>