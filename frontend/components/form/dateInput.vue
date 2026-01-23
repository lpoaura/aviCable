<template>
  <v-date-input
    v-model="formDate"
    :label="label"
    prepend-inner-icon="mdi-calendar"
    prepend-icon=""
    variant="solo"
    density="compact"
    :rules="rules"
    :max="new Date()"
    @change="updateDate"
  />
</template>

<script setup>


const { label, rules } = defineProps({
  label: {
    type: String,
    required: true,
    default: "Date",
  },
  rules: {
    type: Array,
    required: true,
  },
});

const cablesStore = useCablesStore();
const formDate = ref(cablesStore.getFormDate);

// Met à jour la date dans le store et émet l'événement pour le parent
const updateDate = () => {
  cablesStore.setFormDate(formDate.value);
  emit('update:modelValue', formDate.value); // Émet la date au parent
};

// Regarde les changements dans le store et met à jour formDate
watch(
  () => cablesStore.getFormDate,
  (newDate) => {
    console.debug('watch cablesStore.getFormDate', newDate)
    formDate.value = newDate;
  }
);

watch(
  () => formDate.value,
  (newDate) => {
    console.debug('watch formDate', newDate)
    cablesStore.setFormDate(newDate);
  }
);

onMounted(() => {
  if (!cablesStore.getFormDate) {
    cablesStore.setFormDate(new Date())
  }
})

</script>
