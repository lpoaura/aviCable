<template>
  <v-card elevation="0" class="fill-height">
    <v-stepper v-model="step" :items="['Support', 'Diagnostic']" fill-height>
      <template v-slot:item.1 >
        <form-support @nextStep="nextStep"></form-support>
      </template>
      <template v-slot:item.2>
        <form-diagnosis></form-diagnosis>
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
