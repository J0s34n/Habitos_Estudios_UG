import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const routes = [
  { path: '/', component: () => import('../views/BienvenidaView.vue'), meta: { guest: true } },
  { path: '/login', component: () => import('../views/LoginView.vue'), meta: { guest: true } },
  { path: '/registro', component: () => import('../views/RegistroView.vue'), meta: { guest: true } },
  { path: '/buzon', component: () => import('../views/BuzonView.vue') },
  { path: '/menu', component: () => import('../views/MenuView.vue'), meta: { auth: true } },
  { path: '/test/:id', component: () => import('../views/TestView.vue'), meta: { auth: true } },
  { path: '/resultado/:id', component: () => import('../views/ResultadoView.vue'), meta: { auth: true } },
  { path: '/evaluaciones', component: () => import('../views/EvaluacionesView.vue'), meta: { auth: true } },
  { path: '/perfil', component: () => import('../views/PerfilView.vue'), meta: { auth: true } },
  { path: '/admin', component: () => import('../views/AdminDashboard.vue'), meta: { admin: true } },
  { path: '/admin/tests', component: () => import('../views/AdminTests.vue'), meta: { admin: true } },
  { path: '/admin/quejas', component: () => import('../views/AdminQuejas.vue'), meta: { admin: true } },
  { path: '/admin/reportes', component: () => import('../views/AdminReportes.vue'), meta: { admin: true } },
  { path: '/admin/estudiantes', component: () => import('../views/AdminEstudiantes.vue'), meta: { admin: true } },
  { path: '/admin/respuestas', component: () => import('../views/AdminRespuestas.vue'), meta: { admin: true } }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to) => {
  const auth = useAuthStore()
  if (to.meta.auth && !auth.isLoggedIn) return '/login'
  if (to.meta.admin && !auth.isAdmin) return '/menu'
  if (to.meta.guest && auth.isLoggedIn) return '/menu'
  return true
})

export default router