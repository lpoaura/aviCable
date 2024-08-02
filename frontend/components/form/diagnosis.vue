<template>
  <v-card elevation="0" class="fill-height">
    <v-form ref="form" v-model="formValid">
      <v-card-text>
        <v-container>
          <v-row>
            <v-col cols="12">
              <v-date-input v-model="formDate" label="Date de visite" inner-prepend-icon="mdi-calendar" variant="solo"
                density="compact" :rules="[rules.required]" :max="new Date()" />
            </v-col>
            <template v-if="infrastructureType==='point'">
              <v-col cols="12">
                <v-autocomplete v-model="diagData.pole_type_id" chips :items="poleTypes" item-title="label"
                  item-value="id" :rules="[rules.required]" hide-selected :label="$t('support.support-type')" multiple
                  deletable-chips variant="solo" density="compact" />
              </v-col>
              <v-col cols="12" md="6">
                <v-select v-model="diagData.pole_attractivity_id" :items="riskLevels" item-title="label" item-value="id"
                  :rules="[rules.required]" :label="$t('support.attractiveness')" variant="solo" density="compact" />
              </v-col>
              <v-col cols="12" md="6">
                <v-select v-model="diagData.pole_dangerousness_id" :items="riskLevels" item-title="label"
                  item-value="id" :rules="[rules.required]" :label="$t('support.dangerousness')" variant="solo"
                  density="compact" />
              </v-col>
            </template>
            <template v-if="infrastructureType==='line'">
              <v-col cols="12" md="6">
                <v-select v-model="diagData.sgmt_build_integr_risk_id" :items="riskLevels" item-title="label"
                  item-value="id" :rules="[rules.required]" :label="$t('line.buildIntegRisk')" variant="solo"
                  density="compact" />
              </v-col>
              <v-col cols="12" md="6">
                <v-select v-model="diagData.sgmt_moving_risk_id" :items="riskLevels" item-title="label" item-value="id"
                  :rules="[rules.required]" :label="$t('line.movingRisk')" variant="solo" density="compact" />
              </v-col>
              <v-col cols="12" md="6">
                <v-select v-model="diagData.sgmt_topo_integr_risk_id" :items="riskLevels" item-title="label"
                  item-value="id" :rules="[rules.required]" :label="$t('line.topoIntegRisk')" variant="solo"
                  density="compact" />
              </v-col>
              <v-col cols="12" md="6">
                <v-select v-model="diagData.sgmt_veget_integr_risk_id" :items="riskLevels" item-title="label"
                  item-value="id" :rules="[rules.required]" :label="$t('line.vegetIntegRisk')" variant="solo"
                  density="compact" />
              </v-col>
            </template>
            <v-divider />
            <v-col cols="12" class="text-left">
              <strong>{{$t('diagnosis.actions')}}</strong>
            </v-col>


            <v-col cols="12" md="3">
              <v-checkbox v-model="diagData.isolation_advice" :label="$t('support.advice_isol')" density="compact" />
            </v-col>
            <v-col cols="12" md="3">
              <v-checkbox v-model="diagData.dissuasion_advice" :label="$t('support.advice_disrupt')"
                density="compact" />
            </v-col>

            <v-col cols="12" md="3">
              <v-checkbox v-model="diagData.attraction_advice" :label="$t('support.advice_attract')"
                density="compact" />
            </v-col>
            <v-col cols="12" md="3">
              <v-checkbox v-model="diagData.change_advice" :label="$t('support.change_advice')" density="compact" />
            </v-col>
            <v-col cols="12" class="text-left">
              <v-textarea v-model="diagData.technical_proposal" clearable clear-icon="mdi-close-circle"
                :label="$t('diagnosis.technical_proposal')" :rules="[rules.textLength]" rows="2" counter="300"
                variant="solo" density="compact" />
            </v-col>
            <v-divider />
            <v-col cols="12">
              <v-textarea v-model="diagData.remark" clearable clear-icon="mdi-close-circle" :label="$t('app.remark')"
                :rules="[rules.textLength]" rows="2" counter="300" variant="solo" density="compact" />
            </v-col>
          </v-row>
        </v-container>
        <!-- <pre>{{diagData }}</pre> -->
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
import { VDateInput} from 'vuetify/labs/VDateInput'
import type {DiagData, Diagnosis} from '~/types/diagnosis';
import type { NomenclatureItem } from '~/types/nomenclature';
import * as errorCodes from '~/static/errorConfig.json'
import type { ErrorInfo } from '~/store/errorStore';

const emit = defineEmits();
const {t} = useI18n()
const router = useRouter()
const route = useRoute()


const cablesStore = useCablesStore()
const nomenclaturesStore = useNomenclaturesStore()
const errorStore = useErrorsStore()
const formValid=ref(false)
const infrastructureId = computed(() => cablesStore.formInfrastructureId)
const infrastructureType = computed(() => (route.query.type).toLowerCase())
const diagnosisReady=ref(false)
const diagnosisId = computed(() => route.query.id_diagnosis)
const formDate = ref(new Date(Date.now() - new Date().getTimezoneOffset() * 60000))

const diagData : DiagData = reactive({
  date: new Date(Date.now() - new Date().getTimezoneOffset() * 60000),
  remark: '',
  technical_proposal: '',
  infrastructure: infrastructureId.value,
  pole_type_id: [],
  neutralized: false,
  condition_id: null,
  attraction_advice:false,
  dissuasion_advice: false,
  isolation_advice: false,
  media_id: [],
})


//       // rules for form validation
const rules = reactive({
  required: (v: string | number) => !!v || t('valid.required'),
  textLength: (v: string) => (v || '').length <= 300 || `${t('valid.length')}: 300`,
})


// Menu items
const poleTypes = computed(() => nomenclaturesStore.poleTypeItems)
const conditions = computed(() => nomenclaturesStore.conditionItems)
const riskLevels = computed(() => nomenclaturesStore.riskLevelItems)

const initData = async () => {
  if (diagnosisId.value && infrastructureType) {
    const {data:diagnosis} = await useHttp(`/api/v1/cables/diagnosis/${diagnosisId.value}/`, {method: 'get'})
    formDate.value = new Date(diagnosis.value.date)
    const diagdata: DiagData = {
      id : diagnosis.value.id,
      date: diagnosis.value.date,
      remark: diagnosis.value.remark,
      technical_proposal: diagnosis.value.technical_proposal,
      infrastructure: diagnosis.value.infrastructure,
      pole_type_id: diagnosis.value.pole_type?.map((item:NomenclatureItem) => item.id),
      neutralized: diagnosis.value.neutralized,
      condition_id: diagnosis.value.condition?.id,
      attraction_advice:diagnosis.value.attraction_advice,
      dissuasion_advice: diagnosis.value.dissuasion_advice,
      isolation_advice: diagnosis.value.isolation_advice,
      media_id: [],
    }
    console.log('infrastructureType', infrastructureType)
    if (infrastructureType.value==='point') {
      diagdata.pole_attractivity_id = diagnosis.value.pole_attractivity?.id
      diagdata.pole_dangerousness_id = diagnosis.value.pole_dangerousness?.id
    }
    if (infrastructureType.value==="line"){
      diagdata.sgmt_build_integr_risk_id= diagnosis.value.sgmt_build_integr_risk?.id
      diagdata.sgmt_moving_risk_id= diagnosis.value.sgmt_moving_risk?.id
      diagdata.sgmt_topo_integr_risk_id= diagnosis.value.sgmt_topo_integr_risk?.id
      diagdata.sgmt_veget_integr_risk_id= diagnosis.value.sgmt_veget_integr_risk?.id
    }
    Object.assign(diagData, diagdata)
    diagnosisReady.value=true
  }
  // const diagData = null
}


/**
 * addNewDiagnosis(): Method that create new Diagnosis based on forms data (cf.this.diagData)
 * on an existing Support
 *
 * Error handling: A Diagnosis should be created at time of Infrastructure (Point) creation.
 * If Diagnosis creation fails, related Infrastructure (Point) will be deleted.
 * Related Media will also be deleted in this case.
 * Finally, error message is displayed in snackBar through error handling process.
 */
 const createDiagnosis = async () => {
  // Create Media as selected in component form and get list of Ids of created Media
  // const mediaIdList = await createNewMedia()
  try {
    diagData.infrastructure = infrastructureId.value
    diagData.date = formDate.value.toISOString().substring(0, 10) // set Infrastructure (Point) id
    // diagData.media_id = mediaIdList // set Media id list
    // Create Diagnosis
    const {data : diagnosis }= await useHttp('/api/v1/cables/diagnosis/', {method:'post', body: diagData})
    console.debug('newDiagData', diagnosis)
    return diagnosis
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
 * updateDiagnosis(): Metypethod that update Diagnosis based on forms data (cf.this.diagData)
 *
 * Error handling: If Diagnosis update fails, new created Media will be deleted.
 * Finally, error message is displayed in snackBar through error handling process.
 */
const updateDiagnosis = async () => {
  // Create new Media as selected in component form and get list of Ids of created Media
  // const mediaIdList = await createNewMedia()
  try {

    diagData.infrastructure = infrastructureId.value
    diagData.date = formDate.value.toISOString().substring(0, 10)
    // diagData.media_id = mediaIdList // set Media id list
    // Create Diagnosis
    const {data }= await useHttp(`/api/v1/cables/diagnosis/${diagData.id}/`, {method:'put', body: diagData})
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

const moveToNextStep = async () => {
  const diagnosis = diagnosisId.value ?  await updateDiagnosis() : await createDiagnosis()
  if (diagnosis) {
    router.push(`/infrastructures/${infrastructureId.value}`)
  }
};

// watch(infrastructureType,(newVal, _oldVal) => initData())

onMounted(()=> {
  initData()
})
</script>
