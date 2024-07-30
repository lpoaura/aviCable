<template>
  <NuxtLayout name="view">
    <template #map><map-search :edit-mode="true" mode="line" /></template>
    <form-line />
  </NuxtLayout>
</template>
<script setup>
definePageMeta({
  auth: true,
});
</script>
