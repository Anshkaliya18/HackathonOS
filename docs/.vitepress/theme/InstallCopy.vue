<script setup lang="ts">
import { ref } from 'vue'
const copied = ref(false)
async function copy() {
  try { await navigator.clipboard.writeText('curl -fsSL https://github.com/Anshkaliya18/sherpa/releases/download/v2.0.0/install.sh | bash'); copied.value = true; window.setTimeout(() => copied.value = false, 1400) }
  catch { copied.value = false }
}
</script>
<template><div class="install-block"><code>curl -fsSL https://github.com/Anshkaliya18/sherpa/releases/download/v2.0.0/install.sh | bash</code><button type="button" @click="copy" :aria-label="copied ? 'Install command copied' : 'Copy install command'">{{ copied ? 'Copied' : 'Copy' }}</button></div></template>
