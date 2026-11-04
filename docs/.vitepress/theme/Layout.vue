<script setup lang="ts">
import DefaultTheme from 'vitepress/theme'
import ReadingProgress from './ReadingProgress.vue'
const { Layout: ThemeLayout } = DefaultTheme
</script>

<template><component :is="ThemeLayout"><template #layout-top><ReadingProgress /></template></component></template>
