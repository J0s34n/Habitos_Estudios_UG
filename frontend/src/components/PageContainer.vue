<template>
  <div class="w-full px-4 sm:px-6 lg:px-8 xl:px-12 mx-auto"
    :class="ancho">
    <slot />
  </div>
</template>

<script setup>
defineProps({
  ancho: {
    type: String,
    default: 'max-w-7xl'
  }
})
</script>