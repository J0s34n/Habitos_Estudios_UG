<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const usuario = ref(null)

onMounted(() => {
  const usuarioGuardado = localStorage.getItem('usuario')
  if (usuarioGuardado) {
    usuario.value = JSON.parse(usuarioGuardado)
  }
})

const cerrarSesion = () => {
  localStorage.removeItem('usuario')
  router.push('/login')
}
</script>

<template>
  <div class="dashboard">
    <div class="header">
      <h1>Hola: {{ usuario?.nombre || 'Ramon' }}</h1>
      <h2>Bienvenido</h2>
      <button @click="cerrarSesion" class="btn-logout">Cerrar Sesión</button>
    </div>

    <div class="cards-container">
      <!-- Tarjeta: Iniciar Test -->
      <div class="card">
        <img src="" alt="test" />
        <h3>INICIAR UN NUEVO TEST</h3>
        <button class="btn-arrow">→</button>
      </div>

      <!-- Tarjeta: Evaluaciones Pasadas -->
      <div class="card">
        <img src="" alt="evaluaciones" />
        <h3>EVALUACIONES PASADAS</h3>
        <button class="btn-arrow">→</button>
      </div>

      <!-- Tarjeta: Quejas o Sugerencias -->
      <div class="card">
        <img src="" alt="quejas" />
        <h3>QUEJAS O SUGERENCIAS</h3>
        <button class="btn-arrow">→</button>
      </div>

      <!-- Tarjeta: Información Personal -->
      <div class="card">
        <img src="" alt="info" />
        <h3>INFORMACIÓN PERSONAL</h3>
        <button class="btn-arrow">→</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
    html, body, #app {
        margin: 0;
        padding: 0;
        width: 100%;
        height: 100%;
        }

.dashboard {
  min-height: 100vh;
  background: linear-gradient(180deg, #1a4d6d, #2d5a7b);
  color: white;
  padding: 40px;
}

.header {
  margin-bottom: 50px;
  position: relative;
}

.header h1 {
  font-size: 2.5rem;
  margin: 0;
}

.header h2 {
  font-size: 2rem;
  margin: 0;
}

.btn-logout {
  position: absolute;
  top: 0;
  right: 0;
  padding: 10px 20px;
  background: rgba(255, 255, 255, 0.2);
  border: 1px solid white;
  border-radius: 20px;
  color: white;
  cursor: pointer;
}

.cards-container {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 30px;
  max-width: 1200px;
}

.card {
  background: rgba(210, 180, 140, 0.8);
  border-radius: 20px;
  padding: 40px;
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  min-height: 250px;
}

.card h3 {
  color: black;
  font-size: 1.5rem;
  margin: 20px 0;
}

.card img {
  width: 80px;
  height: 80px;
}
 
.btn-arrow {
  position: absolute;
  top: 20px;
  right: 20px;
  background: transparent;
  border: none;
  font-size: 2rem;
  cursor: pointer;
}
</style>