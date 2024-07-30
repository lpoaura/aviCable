<template>
  <v-card class="my-2">
    <v-card-text>
      <v-row>
        <v-col lg="4" md="12">
          <v-autocomplete v-model="equipment.type_id" :items="equipmentType" item-title="label" item-value="id"
            :rules="[rules.required]" hide-selected :label="$t('support.support-type')" variant="solo" density="compact"
            @input="updateEquipmentData()" />
        </v-col>
        <v-col lg="4" md="12">
          <v-text-field v-model="equipment.count" type="number" placeholder="Nombre" variant="solo" density="compact"
            :rules="[rules.required]" min="0" max="100" @input="updateEquipmentData()" /></v-col>
        <v-col lg="4" md="12">
          <v-text-field v-model="equipment.reference" placeholder="Reference" variant="solo" density="compact"
            counter="50" @input="updateEquipmentData()" />
        </v-col>
        <v-col lg="12"><v-textarea v-model="equipment.comment" :rules="[rules.textLength]" placeholder="Commentaire"
            variant="solo" density="compact" rows="2" counter="300" @input="updateEquipmentData()" /></v-col>

      </v-row>
    </v-card-text>

    <v-card-actions>
      <v-spacer /> <v-btn prepend-icon="mdi-delete-circle" color="red" @click="deleteItem()">Supprimer</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script lang="ts" setup>

// const equipment = ref({
//     type: null,
//     remark: null,
//     reference: null,
//     count:null,
// })
// const {equipment} = defineProps(['equipment'])
import { ref, defineProps, defineEmits } from 'vue';

const { t } = useI18n()
const nomenclaturesStore = useNomenclaturesStore()

const equipmentType = computed(() => nomenclaturesStore.equipmentTypeItems)

const rules = reactive({
  required: (v: string | number) => !!v || t('valid.required'),
  textLength: (v: string) => (v || '').length <= 300 || `${t('valid.length')}: 300`,
})

const {index, equipment } = defineProps({
  index: Number,
  equipment:
  {type: Object,required:true}
});

const emit = defineEmits();


const updateEquipmentData = () => {
  emit('update', equipment);
};


// const updateType = (value: string) => {
//   emit('update', { ...equipment, type_id: value });
// };

// const updateCount = (value: string) => {
//   emit('update', { ...equipment, count: value });
// };

// const updateReference = (value: string) => {
//   emit('update', { ...equipment, reference: value });
// };


// const updateRemark = (value: string) => {
//   emit('update', { ...equipment, comment: value });
// };

const deleteItem = () => {
  emit('delete');
};

onMounted(() => {
  equipment.type_id = equipment.type?.id
  console.log('equipment',equipment.type)
})

</script>
