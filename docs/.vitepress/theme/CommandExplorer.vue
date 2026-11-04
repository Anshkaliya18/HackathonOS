<script setup lang="ts">
import { computed, ref } from 'vue'
import manifest from './command-data.generated.json'

const stages = ['All stages', ...new Set(manifest.implemented.map((item) => item.group))]
const selected = ref('All stages')
const query = ref('')
const copied = ref('')
const commands = computed(() => manifest.implemented.filter((item) =>
  (selected.value === 'All stages' || item.group === selected.value) &&
  `${item.command} ${item.description} ${item.group}`.toLowerCase().includes(query.value.toLowerCase())))
async function copy(command: string) {
  try {
    await navigator.clipboard.writeText(`/${command}`)
    copied.value = command
    window.setTimeout(() => copied.value = '', 1400)
  } catch { copied.value = '' }
}
</script>

<template>
  <section class="command-explorer" aria-label="Sherpa command explorer">
    <div class="explorer-controls">
      <label>Filter by stage <select v-model="selected"><option v-for="stage in stages" :key="stage">{{ stage }}</option></select></label>
      <label>Find a command <input v-model="query" type="search" placeholder="Search commands" /></label>
    </div>
    <p class="explorer-count" aria-live="polite">{{ commands.length }} commands</p>
    <ul class="explorer-list">
      <li v-for="item in commands" :key="item.command">
        <div><code>/{{ item.command }}</code><span class="explorer-stage">{{ item.group }}</span><p>{{ item.description }}</p></div>
        <button type="button" :aria-label="`Copy /${item.command}`" @click="copy(item.command)">{{ copied === item.command ? 'Copied' : 'Copy' }}</button>
      </li>
    </ul>
    <p v-if="!commands.length">No commands match this filter.</p>
  </section>
</template>
