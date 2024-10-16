<template>
  <NuxtLayout name="view">
    <template #map>
      <map-search :edit-mode="true" mode="point" />
    </template>
    <form-mortality />
  </NuxtLayout>
</template>

<script setup>
definePageMeta({
  auth: true,
});
</script>
