<template>
  <v-card elevation="0" class="fill-height">
    <v-stepper v-model="step" :items="['Support', 'Diagnostic']" fill-height hide-actions>
      <template #item.1>
        <form-infrastructure :infrastructure-type="infrastructureType" @next-step="nextStep" />
      </template>
      <template #item.2>
        <form-diagnosis :infrastructure-type="infrastructureType" />
      </template>
    </v-stepper>
  </v-card>
</template>

<script setup lang="ts">
const step = ref(1)

const route = useRoute()
const nextStep = () => {
  step.value++;
}

const infrastructureType = computed(() => route.query.type)
</script>

<style>
.required label::after {
  content: "*";
}
</style>
