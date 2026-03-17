<template>
  <div class="min-h-screen flex flex-col items-center justify-center text-white">
    <div class="text-center mb-16">
      <h1 class="text-5xl font-bold mb-4 leading-tight">
        Reconoce y Mejora<br>
        <span class="text-blue-300">Tus Hábitos De Estudio</span>
      </h1>
      <p class="text-blue-200 text-lg">Bienvenido</p>
    </div>
    <div class="flex flex-col gap-4 w-full max-w-xs">
      <RouterLink to="/login"
        class="bg-white text-blue-900 font-bold py-3 px-8 rounded-full text-center
               hover:bg-blue-100 transition-all shadow-lg">
        INICIAR
      </RouterLink>
      <RouterLink to="/buzon"
        class="border border-white text-white py-3 px-8 rounded-full text-center
               hover:bg-white hover:text-blue-900 transition-all">
        Buzón de quejas
      </RouterLink>
    </div>
  </div>
</template>