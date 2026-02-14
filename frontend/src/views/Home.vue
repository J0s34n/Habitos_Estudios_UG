<script setup>
    import { useRouter } from 'vue-router'
    
    const router = useRouter()
    const irLogin = () => {
      router.push('/login')
    }
    </script>


    <!-- App.vue -->
    <!-- App.vue -->
    <!-- App.vue -->
     <template>
    <div class="hero">
    <header class="top-bar">
      <div class="logo">Universidad de Guanajuato</div>
      <button class="btn-outline">Buzón de quejas</button>
    </header>

    <div class="overlay"></div>

    <div class="content">
      <p class="subtitle">Bienvenido</p>
      <h1>
        Reconoce y Mejora<br />
        <span>Tus Hábitos De Estudio</span>
      </h1>
      <button class="btn-primary" @click="irLogin" >Iniciar</button>
      
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
.hero {
  position: fixed;
  inset: 0;
  width: 100vw;
  height: 100vh;
  min-height: 100svh; /* asegura altura completa en móviles */
  overflow: hidden;
  background: linear-gradient(90deg, #062a42, #7e779a);
  color: #ffffff;
  font-family: 'Montserrat', sans-serif;
}

.overlay {
  display: none; /* se elimina el overlay para dejar visible el degradado */
}

.top-bar {
  position: relative;
  z-index: 2;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 40px;
}

.logo {
  font-weight: 600;
  letter-spacing: 1px;
}

.btn-outline {
  background: transparent;
  border: 1px solid #ffffff;
  color: #ffffff;
  padding: 8px 16px;
  border-radius: 20px;
  cursor: pointer;
}

.content {
  position: relative;
  z-index: 2;
  height: calc(100vh - 80px); /* descuenta altura del header */
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  padding: 0 20px;
}

.subtitle {
  letter-spacing: 6px;
  margin-bottom: 20px;
  text-transform: uppercase;
}

h1 {
  font-size: 3.2rem;
  font-weight: 700;
  line-height: 1.3;
  margin-bottom: 40px;
}

h1 span {
  display: block;
}

.btn-primary {
  background: transparent;
  border: 2px solid #ffffff;
  padding: 12px 40px;
  font-size: 1rem;
  letter-spacing: 4px;
  color: #ffffff;
  cursor: pointer;
}

@media (max-width: 768px) {
  h1 {
    font-size: 2.2rem;
  }
}
</style>