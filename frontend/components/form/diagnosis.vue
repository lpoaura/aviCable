<template>
  <v-card elevation="0" class="fill-height">
    <v-form ref="form" v-model="formValid">
      <v-card-text>
        <v-row>
          <v-container>
            <v-card title="Infos" prepend-icon="mdi-information-outline">
              <v-container>
                <v-row>
                  <v-col cols="12">
                    <v-date-input v-model="formDate" label="Date de visite" inner-prepend-icon="mdi-calendar"
                      variant="solo" density="compact" :rules="[rules.required]" :max="new Date()" />
                  </v-col>
                  <v-col cols="12">
                    <v-autocomplete v-model="diagData.arming_id" chips :items="armingItems.sort((a, b) => a.label.localeCompare(b.label))" item-title="label"
                      item-value="id" :rules="[rules.required]" hide-selected :label="$t('armings')" multiple
                      deletable-chips variant="solo" density="compact" />
                  </v-col>
                  <template v-if="infrastructureType === 'point'">
                    <v-col cols="12" md="6">
                      <v-select v-model="diagData.pole_attractivity_id" :items="riskLevels" item-title="label"
                        item-value="id" :rules="[rules.required]" :label="$t('support.attractiveness')" variant="solo"
                        density="compact" />
                    </v-col>
                    <v-col cols="12" md="6">
                      <v-select v-model="diagData.pole_dangerousness_id" :items="riskLevels" item-title="label"
                        item-value="id" :rules="[rules.required]" :label="$t('support.dangerousness')" variant="solo"
                        density="compact" />
                    </v-col>
                  </template>
                  <template v-if="infrastructureType === 'line'">
                    <v-col cols="12" md="4">
                      <v-select v-model="diagData.sgmt_moving_risk_id" :items="riskLevels" item-title="label"
                        item-value="id" :rules="[rules.required]" :label="$t('line.movingRisk')" variant="solo"
                        density="compact" />
                    </v-col>
                    <v-col cols="12" md="4">
                      <v-select v-model="diagData.sgmt_topo_integr_risk_id" :items="riskLevels" item-title="label"
                        item-value="id" :rules="[rules.required]" :label="$t('line.topoIntegRisk')" variant="solo"
                        density="compact" />
                    </v-col>
                    <v-col cols="12" md="4">
                      <v-select v-model="diagData.sgmt_landscape_integr_risk_id" :items="riskLevels" item-title="label"
                        item-value="id" :rules="[rules.required]" :label="$t('line.vegetIntegRisk')" variant="solo"
                        density="compact" />
                    </v-col>
                  </template>
                </v-row>
              </v-container>
              <v-divider />
              <v-container>
                <v-row>
                  <v-col cols="12" class="text-left">
                    <strong>{{ $t('diagnosis.actions') }}</strong>
                  </v-col>
                  <v-col cols="12" md="3">
                    <v-checkbox v-model="diagData.isolation_advice" :label="$t('support.toInsulate')"
                      density="compact" />
                  </v-col>
                  <v-col cols="12" md="3">
                    <v-checkbox v-model="diagData.dissuasion_advice" :label="$t('support.discourage')"
                      density="compact" />
                  </v-col>

                  <v-col cols="12" md="3">
                    <v-checkbox v-model="diagData.attraction_advice" :label="$t('support.providingIncentives')"
                      density="compact" />
                  </v-col>
                  <v-col cols="12" md="3">
                    <v-checkbox v-model="diagData.change_advice" :label="$t('diagnosis.changeAdvice')"
                      density="compact" />
                  </v-col>
                  <v-col cols="12" class="text-left">
                    <v-textarea v-model="diagData.technical_proposal" clearable clear-icon="mdi-close-circle"
                      :label="$t('diagnosis.technicalProposal')" :rules="[rules.textLength]" rows="2" counter="300"
                      variant="solo" density="compact" />
                  </v-col>
                  <v-divider />
                  <v-col cols="12">
                    <v-textarea v-model="diagData.remark" clearable clear-icon="mdi-close-circle" :label="$t('remark')"
                      :rules="[rules.textLength]" rows="2" counter="300" variant="solo" density="compact" />
                  </v-col>
                </v-row>
              </v-container>
            </v-card>
            <!-- <pre>{{diagData }}</pre> -->
          </v-container>
        </v-row>
        <form-images :medias="diagData.media"></form-images>
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
import { VDateInput } from 'vuetify/labs/VDateInput'
import type { DiagData, Diagnosis } from '~/types/cables';
import type { NomenclatureItem } from '~/types/nomenclature';
import type { NotificationInfo } from '~/types/notifications';
import * as errorCodes from '~/static/errorConfig.json'

const { t } = useI18n()
const router = useRouter()
const route = useRoute()


const cablesStore = useCablesStore()
const nomenclaturesStore = useNomenclaturesStore()
const notificationStore = useNotificationStore()
const mediaStore = useMediaStore()

const formValid = ref(false)
const infrastructureId = computed(() => cablesStore.formInfrastructureId)
const infrastructureType = computed(() => route.query.type && typeof route.query.type == 'string' ? (route.query.type).toLowerCase() : '')
const diagnosisReady = ref(false)
const diagnosisId = computed(() => route.query.id_diagnosis)
const formDate = ref(new Date(Date.now() - new Date().getTimezoneOffset() * 60000))
const armingItems = computed(() => nomenclaturesStore.getArmingItems(infrastructureType.value, ''))
// <NomenclatureItem[]>
// const mediaList = ref<Array<number>>([])

const diagData: DiagData = reactive({
  date: new Date(Date.now() - new Date().getTimezoneOffset() * 60000),
  remark: '',
  technical_proposal: '',
  infrastructure: infrastructureId.value,
  arming_id: [],
  neutralized: false,
  condition_id: null,
  change_advice: false,
  attraction_advice: false,
  dissuasion_advice: false,
  isolation_advice: false,
  media_id: [] as number[],
})

//       // rules for form validation
const rules = reactive({
  required: (v: string | number) => !!v || t('valid.required'),
  textLength: (v: string) => (v || '').length <= 300 || `${t('valid.length')}: 300`,
})


// Menu items
// const armings = computed(() => nomenclaturesStore.armingItems)
// const conditions = computed(() => nomenclaturesStore.conditionItems)
const riskLevels = computed(() => nomenclaturesStore.riskLevelItems)

const initData = async () => {
  if (diagnosisId.value && infrastructureType) {
    const { data: diagnosis } = await useApi<Diagnosis>(`/api/v1/cables/diagnosis/${diagnosisId.value}/`, { method: 'get' })
    if (diagnosis.value) {
      formDate.value = new Date(diagnosis.value.date)
      mediaStore.date = formDate.value
      mediaStore.medias = diagnosis.value.media
      const diagdata: DiagData = {
        id: diagnosis.value.id,
        date: diagnosis.value.date,
        remark: diagnosis.value.remark,
        technical_proposal: diagnosis.value.technical_proposal,
        infrastructure: diagnosis.value.infrastructure,
        arming_id: diagnosis.value.arming?.map((item: NomenclatureItem) => item.id),
        neutralized: diagnosis.value.neutralized,
        condition_id: diagnosis.value.condition?.id,
        attraction_advice: diagnosis.value.attraction_advice,
        dissuasion_advice: diagnosis.value.dissuasion_advice,
        isolation_advice: diagnosis.value.isolation_advice,
        change_advice: diagnosis.value.change_advice,
        media_id: [],
      }
      if (infrastructureType.value === 'point') {
        diagdata.pole_attractivity_id = diagnosis.value.pole_attractivity?.id
        diagdata.pole_dangerousness_id = diagnosis.value.pole_dangerousness?.id
      }
      if (infrastructureType.value === "line") {
        diagdata.sgmt_moving_risk_id = diagnosis.value.sgmt_moving_risk?.id
        diagdata.sgmt_topo_integr_risk_id = diagnosis.value.sgmt_topo_integr_risk?.id
        diagdata.sgmt_landscape_integr_risk_id = diagnosis.value.sgmt_landscape_integr_risk?.id
      }
      Object.assign(diagData, diagdata)
      diagnosisReady.value = true
    }
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

const createMedias = async () => {
  return mediaStore.postMedias()
  // const images = mediaStore.postMedias()
  // return images
}

const createDiagnosis = async () => {
  // Create Media as selected in component form and get list of Ids of created Media
  // const mediaIdList = await createNewMedia()
  try {
    diagData.infrastructure = infrastructureId.value
    diagData.date = formDate.value.toISOString().substring(0, 10) // set Infrastructure (Point) id
    diagData.media_id = await createMedias()
    const url = diagData.id ? `/api/v1/cables/diagnosis/${diagData.id}/` : '/api/v1/cables/diagnosis/'
    const method = diagData.id ? 'put' : 'post'
    const { data: diagnosis, error } = await useApi(url, { method: method, body: diagData })
    if (error.value) {
      notificationStore.setInfo({
        type: 'error',
        msg: `${error}`
      })
    } else {
      notificationStore.setInfo({
        type: 'success',
        msg: diagData.id ? 'Diagnostic mis à jour' : 'Diagnostic créé'
      })
    }
    console.debug('newDiagData', diagnosis)
    mediaStore.resetMedias()
    return diagnosis
  } catch (err) {

    console.error('error', err)
    const error: NotificationInfo = {
      type: 'error',
      msg: `${t(`error.${errorCodes.create_point.msg}`)} - ${err}`
    }
    notificationStore.setInfo(error)
  }
}

const moveToNextStep = async () => {
  const diagnosis = await createDiagnosis()
  if (diagnosis) {
    router.push(`/infrastructures/${infrastructureId.value}`)
  }
};

watch(formDate.value, (newVal, _oldVal) => mediaStore.date = newVal)

onMounted(() => {
  initData()
})

onUnmounted(() => {
  mediaStore.resetMedias()
})

</script>
