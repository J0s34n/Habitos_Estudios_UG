<script setup>
import axios from 'axios'
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const nombre = ref('')
const apellido1 = ref('')
const apellido2 = ref('')
const email = ref('')
const password = ref('')

const registrar = async () => {
  try {
    await axios.post('http://127.0.0.1:8000/api/register/', {
      username: email.value,
      first_name: nombre.value,
      last_name: `${apellido1.value} ${apellido2.value}`,
      email: email.value,
      password: password.value
    })

    alert('Registro exitoso')
    router.push('/login')

  } catch (error) {
    alert('Error al registrar usuario')
    console.error(error.response.data)
  }
}
</script>

<template>
  <div class="register-container">

    <!-- BOTÓN VOLVER A LOGIN -->
    <button class="btn-login-top" @click="irLogin">
      INICIO DE SESIÓN
    </button>

    <div class="left">
      <h1>REGISTRO</h1>
    </div>

    <div class="right">
      <div class="card">

        <div class="row">
          <div>
            <label>Nombre</label>
            <input type="text" v-model="nombre"/>
          </div>

          <div>
            <label>Primer Apellido</label>
            <input type="text"  v-model="apellido1"/>
          </div>
        </div>

        <div class="row">
          <div>
            <label>Segundo Apellido</label>
            <input type="text"  v-model="apellido2" />
          </div>

          <div>
            <label>Email</label>
            <input type="email" v-model="email" />
          </div>
        </div>

        <label class="center">Contraseña</label>
        <input type="password" v-model="password" class="center-input" />

        <button class="btn-register-main"  @click="registrar">REGISTRAR</button>
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
.register-container {
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

.btn-login-top {
  position: absolute;
  top: 20px;
  right: 30px;
  background: transparent;
  border: 1px solid white;
  color: white;
  padding: 8px 18px;
  border-radius: 20px;
  cursor: pointer;
}

.left {
  display: flex;
  align-items: center;
  padding-left: 80px;
}

.left h1 {
  font-size: 4rem;
}

.right {
  display: flex;
  justify-content: center;
  align-items: center;
}

.card {
  width: 520px;
  border: 3px solid white;
  border-radius: 30px;
  padding: 30px;
  background: rgba(0, 0, 0, 0.25);
}

.row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 6px;
  text-transform: uppercase;
  letter-spacing: 2px;
}

input {
  width: 100%;
  padding: 10px;
  border-radius: 20px;
  border: 1px solid white;
  background: transparent;
  color: white;
}

.center {
  text-align: center;
  margin-top: 20px;
}

.center-input {
  width: 60%;
  margin: 0 auto;
  display: block;
}

.btn-register-main {
  display: block;
  margin: 30px auto 0;
  padding: 10px 40px;
  border-radius: 20px;
  background: black;
  color: white;
  border: none;
  cursor: pointer;
}
</style>
