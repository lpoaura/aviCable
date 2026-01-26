<template>
  <NuxtLayout name="view">
    <template #map><map-search :edit-mode="false" /></template>
    <display-component />
  </NuxtLayout>
</template>

<script setup lang="ts">
import type { Feature, FeatureCollection } from 'geojson';
import {useDisplay} from 'vuetify'

const {t} = useI18n()
useHead({
  title: `aviCable - ${t('Search')}`,
  meta: [
    { name: 'description', content: 'Home page' }
  ],
})

definePageMeta({
  middleware: 'auth',
})


const {mobile} = useDisplay()
</script>
