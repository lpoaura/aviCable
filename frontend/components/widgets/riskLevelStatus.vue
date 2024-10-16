<template>
  <v-chip prepend-icon="mdi-circle" :color="notationValues(data, t, detail).color">
    {{ notationValues(data, t, detail).label }}
    <v-tooltip :text="t('display.mortalityCases')">
      <template #activator="{ props }">
        <v-icon v-if="dispMortality && data.properties.mortality?.length" color="red" v-bind="props">mdi-coffin</v-icon>
      </template>
    </v-tooltip>

  </v-chip>

</template>

<script setup lang="ts">
import {notationValues} from '~/helpers/levelHelpers'



const {t} = useI18n()
// Define props with default values

const props = defineProps<{
  data: any; // Replace 'any' with the actual type of data if known
  detail?: boolean; // Make detail optional
  displayMortality?: boolean;
}>();

const detail = props.detail ?? false;
const data = props.data;
const dispMortality = props.displayMortality ?? false;

</script>
