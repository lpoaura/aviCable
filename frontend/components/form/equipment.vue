<template>
  <v-container>
    <v-form v-model="valid" lazy-validation>
      <v-container>
        <v-row>
          <v-col lg="4" md="12">
            <v-autocomplete v-model="selectedEquipment.type_id" :items="equipmentItems" item-title="label"
              item-value="id" :rules="[rules.required]" hide-selected :label="$t('forms.equipment')" variant="solo"
              density="compact" @input="updateEquipmentData" />
          </v-col>
          <v-col lg="4" md="12">
            <v-text-field v-model="selectedEquipment.count" type="number" placeholder="Nombre" variant="solo"
              density="compact" :rules="[rules.required]" min="0" max="100" @input="updateEquipmentData" /></v-col>
          <v-col lg="4" md="12">
            <v-text-field v-model="selectedEquipment.reference" placeholder="Reference" variant="solo" density="compact"
              counter="50" @input="updateEquipmentData" />
          </v-col>
          <v-col lg="12"><v-textarea v-model="selectedEquipment.comment" :rules="[rules.textLength]"
              placeholder="Commentaire" variant="solo" density="compact" rows="2" counter="300"
              @input="updateEquipmentData" /></v-col>
        </v-row>
        <v-btn-group>
          <v-btn :disabled="!valid" :prepend-icon="valid ? 'mdi-check' : 'mdi-alert'" color="success"
            @click="cablesStore.addSelectedToEquipments()">{{ t('forms.add') }}</v-btn>
        </v-btn-group>
      </v-container>
    </v-form>
  </v-container>
</template>

<script lang="ts" setup>
import type { Equipment } from '~/types/cables'


const { t } = useI18n()
const route = useRoute()
const nomenclaturesStore = useNomenclaturesStore()
const valid = ref(false)
const cablesStore = useCablesStore()

const { selectedEquipment } = storeToRefs(cablesStore)

const infrastructureType = computed(() => (!!route.query.type && typeof route.query.type === 'string') && (route.query.type).toLowerCase() || '')
const equipmentItems = computed(() => nomenclaturesStore.getEquipmentItems(infrastructureType.value))

const rules = reactive({
  required: (v: string | number) => !!v || t('valid.required'),
  textLength: (v: string) => (v || '').length <= 300 || `${t('valid.length')}: 300`,
})

const { index } = defineProps({
  index: { type: Number, default: 0 },
});

const equipmentData = ref<Equipment>({} as Equipment)


const emit = defineEmits();


const updateEquipmentData = () => {
  emit('update', equipmentData.value);
};


const deleteItem = () => {
  emit('delete');
};

// onMounted(() => {
//   equipmentData.value = { ...equipment }
// })
</script>
