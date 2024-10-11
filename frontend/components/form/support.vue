<template>
  <v-card elevation="0" class="fill-height">
    <v-form ref="form" v-model="formValid">
      <v-card-text>
        <v-container>
          <v-row>
            <v-col cols="12" class="text-left">
              <strong> {{ $t('forms.generalInfrastructure') }}</strong>
            </v-col>
          </v-row>
          <v-row>
            <v-col v-if="!diagnosis" cols="12">
              <v-select v-model="pointData.owner_id" :items="networkOwners" item-title="label" item-value="id"
                :rules="[rules.required]" :label="$t('support.network')" variant="solo" density="compact" required />
            </v-col>

          </v-row>
        </v-container>
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn color="success" :disabled="!formValid" variant="flat" prepend-icon="mdi-content-save-all"
          @click="moveToNextStep">Sauvegarder</v-btn>
      </v-card-actions>
    </v-form>
  </v-card>

</template>

<script lang="ts" setup>
import * as errorCodes from '~/static/errorConfig.json'
import type { ErrorInfo } from '~/store/errorStore';

const emit = defineEmits();

const coordinatesStore = useCoordinatesStore()
const nomenclaturesStore = useNomenclaturesStore()
const cablesStore = useCablesStore()
const errorStore = useErrorsStore()

const {t} = useI18n()

interface Props{
  support?: object
}
const upc = ref(null)
// data
const form = ref(null) // used to get form ref from "<v-form ref="form">"
const formValid = ref(true)

const props = defineProps<Props>()

// Adding operations
const {support}  = props;

const pointData = reactive({
  geom: coordinatesStore.newGeoJSONObject.geometry,
  owner_id: support ? support.value.owner_id : null,
})

const networkOwners = computed(() => nomenclaturesStore.ownerItems)

const rules = reactive({
  required: (v: string | number) => !!v || t('valid.required'),
  requiredOrNotValid: (v: string | number) => v === 0 || !!v || t('valid.required_or_not_valid'),
  latRange: (v: number) => (v >= 40 && v <= 52) || `${t('valid.range')}40 : 52`,
  lngRange: (v: number) => (v >= -20 && v <= 20) || `${t('valid.range')}-20 : 20`,
  textLength: (v: string) => (v || '').length <= 300 || `${t('valid.length')}: 300`,
})


const moveToNextStep = async () => {
  const support = await createNewPoint()
  if (support) {
    emit('nextStep');
  }
};



// const initData = async () => {
//   if (support) {
//     const {data:diagnosis} = await useHttp(`/api/v1/cables/diagnosis/${diagnosisId.value}/`, {method: 'get'})
//
//     const diagdata: DiagData = {
//       id : diagnosis.value.id,
//       date: diagnosis.value.date,
//       remark: diagnosis.value.remark,
//       technicalProposal: diagnosis.value.technicalProposal,
//       infrastructure: diagnosis.value.infrastructure,
//       pole_type_id: diagnosis.value.pole_type?.map((item:NomenclatureItem) => item.id),
//       neutralized: diagnosis.value.neutralized,
//       condition_id: diagnosis.value.condition?.id,
//       attraction_advice:diagnosis.value.attraction_advice,
//       dissuasion_advice: diagnosis.value.dissuasion_advice,
//       isolation_advice: diagnosis.value.isolation_advice,
//       pole_attractivity_id: diagnosis.value.pole_attractivity?.id,
//       pole_dangerousness_id: diagnosis.value.pole_dangerousness?.id,
//       media_id: [],
//     }
//     Object.assign(diagData, diagdata)
//   }
//   // const diagData = null
// }

const createNewPoint = async () => {
  try {
    pointData.geom = coordinatesStore.newGeoJSONObject.geometry
    const {data : support} = await useHttp('/api/v1/cables/points/', {method: 'post', body: pointData})
    cablesStore.setFormSupportId(support.value.properties.id)
    return support.value
  } catch (_err) {
    const error : ErrorInfo = {
      code:errorCodes['create_point']['code'],
      msg:t(`error.${errorCodes.create_point.msg}`)
    }
    errorStore.setError(error )
  }
}
</script>
