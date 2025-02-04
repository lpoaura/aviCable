<template>
  <NuxtLayout name="view">
    <template #map><map-search :edit-mode="true" :mode="infrastructureType?.toLowerCase()" /></template>
    <form-global-infrastructure />
  </NuxtLayout>
</template>

<script lang="ts" setup>
const route=useRoute()

useHead({
  title: `aviCable - Edit`,
  meta: [
    { name: 'description', content: 'Edit infrastructure' }
  ],
})
const infrastructureType = computed(()=> route.query.type || '')
</script>
