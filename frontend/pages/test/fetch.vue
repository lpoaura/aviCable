<script setup>
const abortController = new AbortController();


const { status, execute, refresh } = useAsyncData(
  'testApi',
  () =>
    $fetch('http://localhost:8000/api/v1/cables/operations/', {
      signal: abortController.signal,
    }),
);

const cancelRequest = () => {
  abortController.abort();
};
</script>


<template>
  <v-row>
    <v-container> <span>Status: {{ status }}</span>
      <v-btn @click="execute()">Trigger Request</v-btn>
      <v-btn @click="cancelRequest">Cancel Request</v-btn>
    </v-container>
  </v-row>
</template>
