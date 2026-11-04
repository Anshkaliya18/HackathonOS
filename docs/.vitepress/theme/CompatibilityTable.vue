<script setup lang="ts">
import compatibility from './compatibility-data.generated.json'
</script>
<template>
  <div class="compat-table-wrap"><table class="compat-table"><thead><tr><th scope="col">Agent</th><th scope="col">Integration files</th><th scope="col">Installer scope</th><th scope="col">Runtime</th></tr></thead>
    <tbody><tr v-for="row in compatibility" :key="row.agent"><th scope="row">{{ row.agent }}</th><td>{{ row.integration }}</td><td>{{ row.scope }}</td><td><span class="compat-badge">{{ row.status }}</span></td></tr></tbody>
  </table></div>
</template>
