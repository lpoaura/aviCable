<template>
  <v-chip :prepend-icon="lastOp ? 'mdi-check-circle' : 'mdi-checkbox-blank-circle-outline'"
    :color="lastOp ? 'green' : 'red'">
    {{ lastOp ? (detail ? `${t('neutralizedOn')} ${lastOp.date}` : lastOp.date) : detail ? t('notNeutralized') :
      t('no') }}
  </v-chip>
</template>
<script setup lang="ts">
// import { defineProps, withDefaults, computed } from 'vue';
import type { Operation, Infrastructure } from '~/types/cables';


const { t } = useI18n()

const props = withDefaults(defineProps<{
  data: Infrastructure; // Replace 'any' with the actual type of data if known
  detail: boolean;
}>(), {
  detail: false // Default value for detail
});

const lastOp = computed<Operation | null>(() => {
  return props.data?.properties.operations?.length > 0 ? props.data.properties.operations[0] : null;
});
</script>
