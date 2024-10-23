<template>
  <v-snackbar v-model="snackbar">
    ERR-{{ err.code }}: {{ err.msg }}

    <template v-slot:actions>
      <v-btn color="pink" prepend-icon="mdi-close" @click="snackbar = false">
        Close
      </v-btn>
    </template>
  </v-snackbar>
</template>

<script setup lang="ts">
const { err } = useErrorsStore()

const snackbar = ref(false)

watch(err, (val) => {
  console.error('ERROR snackbar', val)
  snackbar.value = true
})
</script>
