<template>
  <v-container class="fill-height pa-0" fluid>
    <NuxtLayout name="view">
      <template #map>
        <map :edit-mode="false" />
      </template>
      <data-operation-detail :data="data" />
    </NuxtLayout>
  </v-container>
</template>


<script setup>
definePageMeta({
  middleware: 'auth',
  layout: false
})
const route = useRoute()
const { data: data } = await useHttp(`cables/operations/${route.params.id}`)
</script>
