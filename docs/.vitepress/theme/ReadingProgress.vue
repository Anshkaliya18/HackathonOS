<script setup lang="ts">
import { onMounted, onUnmounted, ref } from 'vue'
const progress = ref(0)
let update: (() => void) | undefined
onMounted(() => {
  update = () => {
    const max = document.documentElement.scrollHeight - window.innerHeight
    progress.value = max > 0 ? Math.min(100, Math.max(0, window.scrollY / max * 100)) : 0
  }
  window.addEventListener('scroll', update, { passive: true })
  window.addEventListener('resize', update)
  update()
})
onUnmounted(() => {
  if (update) window.removeEventListener('scroll', update)
  if (update) window.removeEventListener('resize', update)
})
</script>

<template><div class="reading-progress" aria-hidden="true" :style="{ transform: `scaleX(${progress / 100})` }" /></template>
