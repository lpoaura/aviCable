<template>
  <NuxtLayout name="view">
    <template #map>      <map-search :edit-mode="true" mode="point" /></template>
    <v-layout full-height>
      <v-app-bar density="compact" color="blue-grey-lighten-5">
        <v-app-bar-title>
          Edition d'un cas de mortalité
        </v-app-bar-title>
        <v-app-bar-nav-icon>
          <v-btn density="compact" icon="mdi-close" @click="back()" />
        </v-app-bar-nav-icon>
      </v-app-bar>
      <v-main scrollable>
        <v-container>
          <form-mortality />
        </v-container>
      </v-main>
    </v-layout>

  </NuxtLayout>
</template>


<script setup>
useHead({
  titleTemplate : (titleChunk) => {
    return titleChunk ? `${titleChunk} - Mortality edit`:`Mortality edit`;
  }
})

definePageMeta({
  middleware: 'auth',
})
const router = useRouter()

const back = () => {
  router.back()
}
</script>
