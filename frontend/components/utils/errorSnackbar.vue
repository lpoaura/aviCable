<template>
  <div class="text-right">
    <v-snackbar v-model="snackbar" :timeout="timeout" multi-line :color="notificationStore.info?.type || 'info'"
      :icon="`$${notificationStore.info?.type || 'info'}`">
      <v-icon>{{ `$${notificationStore.info?.type || 'info'}` }}</v-icon>
      {{ notificationStore.info?.msg || 'NO MESSAGE'}}
      <template #actions>
        <v-btn icon="mdi-close" color="white" variant="text" @click="snackbar = false" />
      </template>
    </v-snackbar>
  </div>
</template>

<script setup lang="ts">
const notificationStore = useNotificationStore()

const snackbar = ref(false)
const timeout = ref(2000)

watch(() => notificationStore.info, () => {
  console.log('value changes detected')
  snackbar.value = true
})

</script>
