<template>
  <NuxtLayout name="view">
    <template #map><map-search :edit-mode="false" /></template>
    <display-component />
  </NuxtLayout>
</template>

<script setup>
import {ref} from 'vue'
import {useDisplay} from 'vuetify'

definePageMeta({
  auth: true
})

const {mobile} = useDisplay()

onMounted (() => {
  console.debug(`the component is now mounted. mobile`, mobile)
})

</script>
