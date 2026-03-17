import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '../api/axios'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(JSON.parse(localStorage.getItem('user') || 'null'))
  const token = ref(localStorage.getItem('access_token'))

  const isLoggedIn = computed(() => !!token.value)
  const isAdmin = computed(() => user.value?.rol === 'admin')

  async function login(username, password) {
    const { data } = await api.post('/auth/login/', { username, password })
    token.value = data.access
    localStorage.setItem('access_token', data.access)
    localStorage.setItem('refresh_token', data.refresh)
    await fetchPerfil()
  }

  async function fetchPerfil() {
    const { data } = await api.get('/usuarios/perfil/')
    if (data.is_superuser || data.is_staff || data.rol === 'admin') {
      data.rol = 'admin'
    }
    user.value = data
    localStorage.setItem('user', JSON.stringify(data))
  }

  async function registro(datos) {
    await api.post('/usuarios/registro/', datos)
  }

  function logout() {
    user.value = null
    token.value = null
    localStorage.clear()
  }

  return { user, token, isLoggedIn, isAdmin, login, registro, logout, fetchPerfil }
})