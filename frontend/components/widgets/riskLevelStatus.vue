<template>
  <v-chip prepend-icon="mdi-circle" :color="notationValues(props.data, t, detail).color">
    {{ notationValues(props.data, t, detail).label }}
  </v-chip>
</template>

<script setup lang="ts">
import {notationValues} from '~/helpers/levelHelpers'



const {t} = useI18n()
// Define props with default values

const props = defineProps<{
  data: any; // Replace 'any' with the actual type of data if known
  detail?: boolean; // Make detail optional
}>();

const detail = props.detail ?? false;

</script>
