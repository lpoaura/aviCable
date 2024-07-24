<template>
  <v-card title="equipement">
    <v-container>
      <v-row>
        <v-col lg="6" md="12">
          <v-autocomplete v-model="equipment.type_id" :items="equipmentType" item-title="label" item-value="id"
            :rules="[rules.required]" hide-selected :label="$t('support.support-type')" variant="solo" density="compact"
            @input="updateType($event.target.value)"></v-autocomplete>
            <p>{{ equipment.type_id }}</p>
        </v-col>
        <v-col lg="6" md="12">
          <v-text-field type="number" v-model="equipment.count" placeholder="Nombre" variant="solo" density="compact"
            :rules="[rules.required]" @input="updateCount($event.target.value)"></v-text-field></v-col>
        <v-col lg="12">
          <v-text-field v-model="equipment.reference" placeholder="Reference" variant="solo" density="compact"
            @input="updateReference($event.target.value)"></v-text-field>
        </v-col>
        <v-col lg="12"><v-text-field v-model="equipment.comment" :rules="[rules.textLength]" placeholder="Commentaire"
            variant="solo" density="compact" @input="updateRemark($event.target.value)"></v-text-field></v-col>
      </v-row>
    </v-container>
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
const { t } = useI18n()
const nomenclaturesStore = useNomenclaturesStore()

const equipmentType = computed(() => nomenclaturesStore.equipmentTypeItems)

const rules = reactive({
  required: (v: string | number) => !!v || t('valid.required'),
  textLength: (v: string) => (v || '').length <= 300 || `${t('valid.length')}: 300`,
})

import { ref, defineProps, defineEmits } from 'vue';

const {index, equipment } = defineProps({
  index: Number,
  equipment:
  {type: Object,required:true}
});

const emit = defineEmits();

const updateType = (value: string) => {
  emit('update', { ...equipment, type_id: value });
};

const updateCount = (value: string) => {
  emit('update', { ...equipment, count: value });
};

const updateReference = (value: string) => {
  emit('update', { ...equipment, reference: value });
};


const updateRemark = (value: string) => {
  emit('update', { ...equipment, comment: value });
};

onMounted(() => {
  equipment.type_id = equipment.type?.id
  console.log('equipment',equipment.type)
})

</script>
