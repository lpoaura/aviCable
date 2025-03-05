<template>
  <v-app dark>
    <h1 v-if="error.statusCode === 404">
      {{ pageNotFound }}
    </h1>
    <h1 v-else>
      {{ otherError }}
    </h1>
    <h2>
      {{ error.message }}
    </h2>
    <NuxtLink to="/">
      Home page
    </NuxtLink>
  </v-app>
</template>

<script lang="ts" setup>
/**
 * Default Nuxt page. Not still modified
 */

import type { NotificationInfo } from '~/types/notifications'

const pageNotFound = ref('404 Not Found')
const otherError = ref('An error occurred')

useHead({
  title: error.code === 404 ? pageNotFound : otherError,
  meta: [
    { name: 'description', content: 'Error' }
  ],
})

const { error } = defineProps<Props>()
const props = useProps()
</script>

<style scoped>
h1 {
  font-size: 20px;
}
</style>
