<template>
  <v-container class="fill-height pa-0" fluid>
    <NuxtLayout name="view">
      <template #map>
        <map-search :edit-mode="false" />
      </template>
      <data-line-detail :data="data" />
    </NuxtLayout>
  </v-container>
</template>


<script setup>
definePageMeta({
  middleware: 'auth',
  layout: false
})
const route = useRoute()
const { data: data } = await useHttp(`/api/v1/cables/infrastructures/${route.params.id}`)
</script>
