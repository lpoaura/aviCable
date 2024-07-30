<template>
  <v-card elevation="0" class="fill-height">
    <v-form ref="form" v-model="formValid">
      <v-card-text>
        <v-row>
          <v-col cols="12" md="6">
            <v-date-input v-model="formDate" :locale="currentLocale.iso" label="Date de visite"
              inner-prepend-icon="mdi-calendar" variant="solo" density="compact" :rules="[rules.required]"
              :max="new Date()" />
          </v-col>
          <v-col cols="12" md="6">
            <v-select v-model="opData.operation_type_id" :items="operationType" item-title="label" item-value="id"
              :rules="[rules.required]" :label="`Type d'opération`" variant="solo" density="compact" />
          </v-col>
          <v-col cols="12">
            <v-textarea v-model="opData.remark" clearable clear-icon="mdi-close-circle" :label="$t('app.remark')"
              :rules="[rules.textLength]" rows="2" counter="300" variant="solo" density="compact" />
          </v-col>
          <v-col cols="12">
            <p><strong>Equipements</strong></p>
            <div v-for="(equipment, index) in opData.equipments" :key="index">
              <form-equipment :equipment="equipment" :index="index" @update="updateEquipmentData(index, $event)"
                @delete="deleteEquipment(index)" />
            </div>

          </v-col>
        </v-row>

      </v-card-text>
      <v-card-actions>
        <v-spacer /><v-btn color="info" variant="flat" prepend-icon="mdi-plus-circle"
          @click="newEquipment">équipement</v-btn> <v-btn color="success" :disabled="!formValid" variant="flat"
          prepend-icon="mdi-content-save-all" @click="submit">Sauvegarder</v-btn>
      </v-card-actions>
    </v-form>
    <pre>{{ opData }}</pre>
  </v-card>
</template>

<script lang="ts" setup>
import { VDateInput} from 'vuetify/labs/VDateInput'
// import type {DiagData, Diagnosis} from '~/types/diagnosis';
import * as errorCodes from '~/static/errorConfig.json'
import type { ErrorInfo } from '~/store/errorStore';

const emit = defineEmits();
const {t, locales} = useI18n()
const router = useRouter()
const route = useRoute()

const coordinatesStore = useCoordinatesStore()
const cablesStore = useCablesStore()
const nomenclaturesStore = useNomenclaturesStore()
const errorStore = useErrorsStore()
const formValid=ref(false)
const supportId = computed(() => cablesStore.getFormSupportId)
const operationId = computed(() => route.query.id_operation)
const formDate = ref(new Date(Date.now() - new Date().getTimezoneOffset() * 60000))
const opData = reactive({
  date: (new Date(Date.now() - new Date().getTimezoneOffset() * 60000)).toISOString().substring(0,10),
  remark: '',
  infrastructure: supportId.value,
  operation_type_id: null,
  equipments: [{
    id: null,
    type_id: null,
    count:null,
    reference: null,
    comment: null,
  }],
  media: [],
  resourcetype: 'PointOperation',
  geom: null,
})

const updateEquipmentData = (index, updatedEquipment) => {
      opData.equipments.value[index] = updatedEquipment;
    };

const deleteEquipment=(index) => {
  console.log("opData.equipments.value", opData.equipments)
  opData.equipments.splice(index,1)
}

const newEquipment = () => {
  const eq = {
    id: null,
    type: null,
    count:1,
    reference: null,
    comment: null,
  }
  opData.equipments.push(eq)
}

const locale = useLocale()
const currentLocale = computed(() => locales.value.find(item => item.code == locale.value))
const newGeoJSONObject = computed(() => coordinatesStore.newGeoJSONObject)

watch(newGeoJSONObject, (value) => {
  if (value) {
  opData.geom = value.geometry
  }
})
//       // rules for form validation
const rules = reactive({
  required: (v: string | number) => !!v || t('valid.required'),
  textLength: (v: string) => (v || '').length <= 300 || `${t('valid.length')}: 300`,
})


// Menu items
const operationType = computed(() => nomenclaturesStore.operationTypeItems)

const initData = async () => {
  if (supportId.value && !operationId.value) {
    const {data:support} = await useHttp(`/api/v1/cables/infrastructures/${supportId.value}/`, {method: 'get'})
    coordinatesStore.setNewGeoJSONObject(support)
    if (!opData.geom) {
      opData.geom = coordinatesStore.newGeoJSONObject.geometry
    }
  }
  if (operationId.value) {
    const {data:operation} = await useHttp(`/api/v1/cables/operations/${operationId.value}/`, {method: 'get'})
    formDate.value = new Date(operation.value.properties.date)
    const opdata = {
      id : operation.value.properties.id,
      remark: operation.value.properties.remark,
      infrastructure: supportId.value,
      operation_type_id: operation.value.properties.operation_type?.id,
      equipments: operation.value.properties.equipments,
      media: operation.value.properties.media.map(item => item.id),
      resourcetype: operation.value.resourcetype,
      geom: operation.value.geometry,
    }
    Object.assign(opData, opdata)
    coordinatesStore.setNewGeoJSONPoint(operation.value.geometry)
    coordinatesStore.setSelectedFeature(operation.value)
  }
  // const opData = null
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
    opData.infrastructure = supportId.value
    opData.date = formDate.value.toISOString().substring(0, 10) // set Infrastructure (Point) id
    // opData.media_id = mediaIdList // set Media id list
    // Create Diagnosis
    const {data : operation }= await useHttp('/api/v1/cables/operations/', {method:'post', body: opData})
    console.debug('newDiagData', operation)
    return operation
  } catch (_err) {

    console.error ('error',_err)
    const error : ErrorInfo = {
      code:errorCodes['create_point']['code'],
      msg:t(`error.${errorCodes.create_point.msg}`)
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
  // Create new Media as selected in component form and get list of Ids of created Media
  // const mediaIdList = await createNewMedia()
  try {

    opData.infrastructure = supportId.value
    opData.date = formDate.value.toISOString().substring(0, 10)
    opData.resourcetype = 'PointOperation',
    opData.geom = coordinatesStore.newGeoJSONPoint
    // opData.media_id = mediaIdList // set Media id list
    // Create Diagnosis
    const {data}= await useHttp(`/api/v1/cables/operations/${operationId.value}/`, {method:'put', body: opData})
    return data
  } catch (_err) {
    // If Diagnosis creation fails, related Media created are deleted
    // if (mediaIdList) {
    //   mediaIdList.forEach(
    //       async (media_id) => await this.$axios.$delete(`/media/${media_id}/`)
    //   )
    // }
    // Error display
    console.error ('error',_err)
    const error : ErrorInfo = {
      code: errorCodes['update_pole_diagnosis']['code'],
      msg:t(`error.${errorCodes['update_pole_diagnosis']['msg']}`)
    }
    errorStore.setError(error)
  }
}

const submit = async () => {
  const operation = operationId.value ?  await updateOperation() : await createOperation()
  if (operation) {
    router.push(`/supports/${supportId.value}`)
  }
};


onMounted(()=> {
  initData()
})
</script>
