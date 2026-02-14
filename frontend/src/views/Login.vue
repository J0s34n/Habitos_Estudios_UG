<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router';
import axios from 'axios'
const router = useRouter()

const email = ref('')
const password = ref('')

const login = async () => {
  try {
    const response = await axios.post('http://127.0.0.1:8000/api/login/', {
      email: email.value,
      password: password.value
    })

    console.log(response.data)

    // Guardamos el usuario (opcional pero recomendado)
    localStorage.setItem('usuario', JSON.stringify(response.data))

    // 🔥 AQUÍ REDIRIGES
    router.push('/dashboard')

  } catch (error) {
    alert('Credenciales incorrectas')
    console.error(error)
  }
}
</script>
 
<template>
  <div class="login-container">
    <!-- BOTÓN REGISTRO -->
    <button class="btn-register" @click="router.push('/register')">REGISTRARSE</button>

    <div class="left">
      <h1>INICIO DE<br />SESIÓN</h1>
    </div>

    <div class="right">
      <div class="card">
        <label>Usuario</label>
        <input type="text" v-model="email" />

        <label>Contraseña</label>
        <input type="password" v-model="password" />

        <button class="btn-login" @click="login">INICIAR</button>
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
        
  .login-container {
    position: fixed;
    inset: 0;
    width: 100vw;
    height: 100vh;
    min-height: 100svh; 
    overflow: hidden;
    
    min-height: 100vh;
    display: grid;
    grid-template-columns: 1fr 1fr;
    background: linear-gradient(90deg, #062a42, #7e779a);
    color: white;
    
  }
  .btn-register {
    position: absolute;
    top: 20px;
    right: 30px;
    padding: 8px 18px;
    border-radius: 20px;
    background: transparent;
    border: 1px solid white;
    color: white;
    font-size: 0.8rem;
    letter-spacing: 1px;
    cursor: pointer;
  }
  
  .left {
    display: flex;
    align-items: center;
    padding-left: 80px;
  }
  
  .left h1 {
    font-size: 3.5rem;
  }
  
  .right {
    display: flex;
    justify-content: center;
    align-items: center;
  }
  
  .card {
    width: 320px;
    border: 2px solid white;
    border-radius: 20px;
    padding: 30px;
    background: rgba(0, 0, 0, 0.2);
  }
  
  label {
    display: block;
    margin-top: 20px;
    margin-bottom: 6px;
  }
  
  input {
    width: 100%;
    padding: 10px;
    border-radius: 20px;
    border: 1px solid white;
    background: transparent;
    color: white;
  }
  
  .btn-login {
    margin-top: 30px;
    width: 100%;
    padding: 10px;
    border-radius: 20px;
    background: black;
    color: white;
    border: none;
    cursor: pointer;
  }
  </style>