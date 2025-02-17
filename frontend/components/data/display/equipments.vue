<template>
  <v-list lines="two">
    <v-list-item v-for="(equipment, index) in equipments" :key="index">
      <template #title><v-chip>{{ equipmentTypeValues(equipment)?.code }} </v-chip> {{
        equipmentTypeValues(equipment)?.label }} <strong>x{{
          equipment.count }}</strong>
      </template>
      <div v-if="equipment.reference"><strong>{{ $t("reference") }}</strong>&nbsp;: {{ equipment.reference }}
      </div>
      <div v-if="equipment.comment"><strong>{{ $t("remark") }}</strong>&nbsp;: {{ equipment.comment }}</div>
      <template v-slot:append v-if="edit">
        <v-btn color="blue-lighten-1" icon="mdi-pencil" variant="text" size="small"
          @click="selectedEquipment = formEquipments[index]"></v-btn>
        <v-btn color="red-lighten-1" icon="mdi-trash-can" variant="text" size="small"
          @click="formEquipments.splice(index, 1)"></v-btn>
      </template>
    </v-list-item>
  </v-list>
</template>

<script setup lang="ts">
import type { Equipment } from '~/types/cables';
import type { Nomenclature } from '~/types/nomenclature';

const { equipments } = defineProps<{
  equipments: Equipment[];
  edit: boolean;
}>();

const cablesStore = useCablesStore()
const { selectedEquipment, formEquipments } = storeToRefs(cablesStore)

const nomenclaturesStore = useNomenclaturesStore()

const { equipmentTypeItems } = storeToRefs(nomenclaturesStore)

const equipmentTypeValues: Nomenclature | undefined = (equipment: Equipment) => {
  const id = equipment.type_id || equipment.type?.id
  return equipmentTypeItems.value?.find(item => item.id == id)
}

</script>
