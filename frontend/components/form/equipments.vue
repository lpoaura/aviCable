<template>
  <v-row>
    <v-container>
      <v-card :title="t('Equipments')" prepend-icon="mdi-camera">
        <data-display-equipments :equipments="formEquipments" :edit="true" />
        <v-divider></v-divider>
        <form-equipment v-if="edit" />
        <v-divider></v-divider>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn prepend-icon="mdi-camera-plus-outline" @click="addEquipment()" color="info">
            {{ t('forms.Equipment') }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-container>
  </v-row>
</template>

<script lang="ts" setup>
import type { Equipment } from '~/types/cables'

const { t } = useI18n()

const cablesStore = useCablesStore()
const { formEquipments, selectedEquipment } = storeToRefs(cablesStore)

// const emit = defineEmits()
const addEquipment = () => {
  // cablesStore.addSelectedToEquipments()
  // mediaStore.resetSelectedMedia()
  if (selectedEquipment) {
    selectedEquipment.value = {} as Equipment
  }
}

const edit = ref(false)

watch(
  () => selectedEquipment.value,
  (newValue, _oldValue) => {
    edit.value = !!newValue
  },
)

</script>
