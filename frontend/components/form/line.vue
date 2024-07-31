<template>
  <v-card elevation="0" class="fill-height">
    <v-stepper v-model="step" :items="['Ligne', 'Diagnostic']" fill-height hide-actions>
      <template #item.1>
        <form-infrastructure type="lines" @next-step="nextStep" />
      </template>
      <template #item.2>
        <form-diagnosis type="lines" />
      </template>
    </v-stepper>
  </v-card>
</template>

<script setup lang="ts">
const step = ref(1)

const nextStep= () => {
  step.value++;
}

</script>

<style>
.required label::after {
  content: "*";
}
</style>
