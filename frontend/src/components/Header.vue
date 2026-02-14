<template>
    <header class="header">
      <!-- Lado izquierdo: imagen -->
      <div class="header-left">
        <img
          src="/logo.png"
          alt="Logo"
          class="header-logo"
        />
      </div>
  
      <!-- Lado derecho: botón circular -->
      <div class="header-right">
        <button class="complaint-button">
          Buzón de<br />quejas
        </button>
      </div>
    </header>
  </template>
  
  <script setup>
  // Por ahora no se requiere lógica
  </script>
  
  <style scoped>
  .header {
    width: 100%;
    height: 80px;
    padding: 0 24px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: #ffffff;
    border-bottom: 1px solid #e0e0e0;
  }
  
  /* Imagen izquierda */
  .header-logo {
    height: 55px;
    object-fit: contain;
  }
  
  /* Botón circular */
  .complaint-button {
    width: 90px;
    height: 90px;
    border-radius: 50%;
    background-color: #1e88e5;
    color: #ffffff;
    font-size: 13px;
    font-weight: 600;
    border: none;
    cursor: pointer;
    text-align: center;
    line-height: 1.2;
    transition: background-color 0.3s ease;
  }
  
  .complaint-button:hover {
    background-color: #1565c0;
  }
  </style>
  