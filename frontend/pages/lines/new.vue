<template>
  <v-container class="fill-height pa-0" fluid>
    <NuxtLayout name="view">
      <template #map>
        <map-search :edit-mode="true" mode="line" />
      </template>
      <form-line />
    </NuxtLayout>
  </v-container>
</template>

<script setup>
definePageMeta({
  middleware: 'auth',
  layout: false
})
</script>
