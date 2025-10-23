<template>
  <v-chip :prepend-icon="prependIcon" :color="color">
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

const prependIcon = computed<string>(() => {
  if (lastOp.value) {
    return (
      lastOp.value.neutralization_level == 'full' ?
        'mdi-check-circle' : lastOp.value.neutralization_level == 'partial' ?
          'mdi-check' : 'mdi-checkbox-blank-circle-outline')
  }
  return 'mdi-checkbox-blank-circle-outline'
})

const color = computed<string>(() => {
  // si neutralisé
  if (lastOp.value && lastOp.value.neutralization_level) {
    return (
      lastOp.value.neutralization_level == 'full' ?
        'green' : 'yellow')
  }
  // TODO: Si on a un risque faible, alors on met en gris
  
  // sinon
  return 'red'
})
</script>
