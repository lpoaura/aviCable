<template>
  <v-chip prepend-icon="mdi-circle" :color="notationValues(data, t, detail).color">
    {{ notationValues(data, t, detail).label }}
  </v-chip>
</template>

<script setup lang="ts">
import {notationValues} from '~/helpers/levelHelpers'



const {t} = useI18n()
// Define props with default values

const {data, detail} = withDefaults(defineProps<{
  data: any; // Replace 'any' with the actual type of data if known
  detail: boolean;
}>(), {
  detail: false // Default value for detail
});




</script>
