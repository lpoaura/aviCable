<template>
  <v-card elevation="0" class="fill-height">
    <v-form ref="form" v-model="formValid">
      <v-card-text>
        <v-row>
          <v-container>
            <v-card title="infos" prepend-icon="mdi-information">
              <v-container>
                <v-date-input v-model="formDate" :locale="currentLocale.iso" label="Date de visite"
                prepend-icon="" prepend-inner-icon="mdi-calendar" variant="solo" density="compact" :rules="[rules.required]"
                  :max="new Date()" />
                <v-textarea v-model="opData.remark" clearable clear-icon="mdi-close-circle" :label="$t('remark')"
                  :rules="[rules.textLength]" rows="2" counter="300" variant="solo" density="compact" />
              </v-container>
            </v-card>
          </v-container>
        </v-row>
        <form-equipments></form-equipments>
        <form-images :medias="opData.media" @update="getFormMedias"></form-images>
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn color="success" :disabled="!formValid" variant="flat" prepend-icon="mdi-content-save-all"
          @click="submit">Sauvegarder</v-btn>
      </v-card-actions>
    </v-form>
  </v-card>
</template>

<script lang="ts" setup>
import { storeToRefs } from 'pinia';
// import { VDateInput } from 'vuetify/labs/VDateInput'
// import type {DiagData, Diagnosis} from '~/types/diagnosis';
import * as errorCodes from '~/static/errorConfig.json'
import type { ErrorInfo } from '~/store/errorStore';
import type { OperationFeature, Operation } from '~/types/cables';
import type { Feature } from 'geojson';

const emit = defineEmits();
const { t, locales } = useI18n()
const router = useRouter()
const route = useRoute()

const coordinatesStore = useCoordinatesStore()
const cablesStore = useCablesStore()
const nomenclaturesStore = useNomenclaturesStore()
const errorStore = useErrorsStore()
const mediaStore = useMediaStore()
const formValid = ref(false)
const medias = ref<Array<Media>>([])

const { newGeoJSONObject, selectedFeature } = storeToRefs(coordinatesStore)
const { formInfrastructure } = storeToRefs(cablesStore)

const infrastructureId = computed(() => {
  const id = route.params.id;
  if (typeof id === 'string') {
    return parseInt(id);
  } else if (Array.isArray(id)) {
    return parseInt(id[0]);
  }
  return NaN;
});
const infrastructure = computed(() => formInfrastructure.value)
const operationId = computed(() => route.query.id_operation)
const formDate = ref(new Date(Date.now() - new Date().getTimezoneOffset() * 60000))
const equipmentsReady = ref(false)
const opData = reactive<Operation>({
  date: (new Date(Date.now() - new Date().getTimezoneOffset() * 60000)).toISOString().substring(0, 10),
  remark: '',
  infrastructure: infrastructureId.value,
  equipments: [{
    id: null,
    type_id: null,
    count: 1,
    reference: null,
    comment: null,
  }],
  media: [],
  geom: null,
})


const updateEquipmentData = (index, updatedEquipment) => {
  opData.equipments[index] = updatedEquipment;
};

//const deleteEquipment = (index) => {
//  opData.equipments.splice(index, 1)
// }

// const newEquipment = () => {
//   const eq = {
//     id: null,
//     type: null,
//     count: 1,
//     reference: null,
//     comment: null,
//   }
//   opData.equipments.push(eq)
// }

const locale = useLocale()
const currentLocale = computed(() => locales.value.find(item => item.code == locale.value))

watch(newGeoJSONObject, (value: Feature) => {
  if (value) {
    opData.geom = value.geometry
  }
})
//       // rules for form validation
const rules = reactive({
  required: (v: string | number) => !!v || t('valid.required'),
  textLength: (v: string) => (v || '').length <= 300 || `${t('valid.length')}: 300`,
})



const initData = async () => {
  if (infrastructureId.value && !operationId.value) {
    opData.resourcetype = infrastructure.value?.resourcetype === 'Point' ? 'PointOperation' : 'LineOperation'
    equipmentsReady.value = true
  }
  if (operationId.value) {
    const { data: operation } = await useApi<OperationFeature>(`/api/v1/cables/operations/${operationId.value}/`, { method: 'get' })
    if (operation.value) {
      formDate.value = new Date(operation.value.properties.date)
      mediaStore.date = formDate.value
      mediaStore.medias = operation.value.properties.media
      const opdata = {
        id: operation.value.properties.id,
        remark: operation.value.properties.remark,
        infrastructure: operation.value.properties.infrastructure,
        equipments: operation.value.properties.equipments.map(item => {
          item.type_id = item.type?.id
          // delete item['type']
          return item
        }),
        // equipments: operation.value.properties.equipments,
        media: operation.value.properties.media.map(item => item.id),
        resourcetype: operation.value.resourcetype,
        geom: operation.value.geometry,
      }
      cablesStore.formEquipments = operation.value.properties.equipments
      Object.assign(opData, opdata)
      selectedFeature.value = operation.value
      equipmentsReady.value = true
    }
  }
  // const opData = null
}

const createMedias = async () => {
  return mediaStore.postMedias()
  // const images = mediaStore.postMedias()
  // return images
}
/**
 * addNewDiagnosis(): Method that create new Diagnosis based on forms data (cf.this.opData)
 * on an existing Support
 *
 * Error handling: A Diagnosis should be created at time of Infrastructure (Point) creation.
 * If Diagnosis creation fails, related Infrastructure (Point) will be deleted.
 * Related Media will also be deleted in this case.
 * Finally, error message is displayed in snackBar through error handling process.
 */
const createOperation = async () => {
  // Create Media as selected in component form and get list of Ids of created Media
  // const mediaIdList = await createNewMedia()
  try {
    opData.infrastructure = infrastructureId.value
    opData.date = formDate.value.toISOString().substring(0, 10) // set Infrastructure (Point) id
    opData.geom = newGeoJSONObject.value?.geometry || infrastructure.value?.geometry
    opData.media = await createMedias()
    opData.equipments = cablesStore.formEquipments
    // opData.media_id = mediaIdList // set Media id list
    // Create Diagnosis
    const { data: operation } = await useApi('/api/v1/cables/operations/', { method: 'post', body: opData })
    console.debug('newDiagData', operation)
    mediaStore.resetMedias()
    return operation
  } catch (_err) {

    console.error('error', _err)
    const error: ErrorInfo = {
      code: errorCodes['create_point']['code'],
      msg: t(`error.${errorCodes.create_point.msg}`)
    }
    errorStore.setError(error)
  }
}

/**
 * updateDiagnosis(): Method that update Diagnosis based on forms data (cf.this.opData)
 *
 * Error handling: If Diagnosis update fails, new created Media will be deleted.
 * Finally, error message is displayed in snackBar through error handling process.
 */
const updateOperation = async () => {

  try {
    opData.date = formDate.value.toISOString().substring(0, 10)
    opData.media = await createMedias()
    const { data } = await useApi(`/api/v1/cables/operations/${operationId.value}/`, { method: 'put', body: opData })
    return data
  } catch (_err) {

    console.error('error', _err)
    const error: ErrorInfo = {
      code: errorCodes['update_pole_diagnosis']['code'],
      msg: t(`error.${errorCodes['update_pole_diagnosis']['msg']}`)
    }
    errorStore.setError(error)
  }
}

const getFormMedias = (value) => {
  medias.value = value
}

watch(formDate.value, (newVal, _oldVal) => mediaStore.date = newVal)

const moveToNextStep = async () => {
  const diagnosis = diagnosisId.value ? await updateDiagnosis() : await createDiagnosis()
  if (diagnosis) {
    router.push(`/infrastructures/${infrastructureId.value}`)
  }
};
const submit = async () => {
  const operation = operationId.value ? await updateOperation() : await createOperation()
  if (operation) {
    router.push(`/infrastructures/${infrastructureId.value}`)
  }
};


onMounted(async () => {
  await initData()
})

onUnmounted(() => {
  mediaStore.resetMedias()
})
</script>
