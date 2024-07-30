<template>
  <v-card elevation="0" class="fill-height">
    <v-stepper v-model="step" :items="['Support', 'Diagnostic']" fill-height hide-actions>
      <template #item.1>
        <form-support @next-step="nextStep" />
      </template>
      <template #item.2>
        <form-diagnosis />
      </template>
    </v-stepper>
  </v-card>
</template>

<script setup lang="ts">
const step = ref(1)

const nextStep= () => {
  console.log('STEP', step)
  step.value++;
}

</script>

<style>
.required label::after {
  content: "*";
}
</style>
