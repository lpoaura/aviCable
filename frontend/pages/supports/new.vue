<template>
  <v-container class="fill-height pa-0" fluid>
    <NuxtLayout name="view">
      <template #map><map-search :edit-mode="true" mode="point" /></template>
      <form-point />
    </NuxtLayout>
  </v-container>
</template>

<script setup lang="ts">
definePageMeta({
  middleware: 'auth',
  layout: false
})
</script>
