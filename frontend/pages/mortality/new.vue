<template>
  <v-container class="fill-height pa-0" fluid>
    <NuxtLayout name="view">
      <template #map>
        <map-search :edit-mode="true" mode="point" />
      </template>
      <form-mortality />
    </NuxtLayout>
  </v-container>
</template>

<script setup>
definePageMeta({
  middleware: 'auth',
  layout: false
})
</script>
