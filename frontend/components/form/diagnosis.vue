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
                    <form-date-input :rules="[rules.required]" label="Date de visite" />
                  </v-col>
                  <v-col cols="12">
                    <v-autocomplete v-model="diagData.arming_id" chips
                      :items="armingItems.sort((a, b) => a.label.localeCompare(b.label))" item-title="label"
                      item-value="id" :rules="[rules.required]" hide-selected :label="$t('armings')" multiple
                      deletable-chips variant="solo" density="compact" />
                  </v-col>
                  <template v-if="infrastructureType === 'point'">
                    <v-col cols="12" md="6">
                      <v-select v-model="diagData.pole_attractivity_id" :items="riskLevels" item-title="label"
                        item-value="id" :rules="[rules.required]" :label="$t('infrastructure.attractiveness')"
                        variant="solo" density="compact" />
                    </v-col>
                    <v-col cols="12" md="6">
                      <v-select v-model="diagData.pole_dangerousness_id" :items="riskLevels" item-title="label"
                        item-value="id" :rules="[rules.required]" :label="$t('infrastructure.dangerousness')"
                        variant="solo" density="compact" />
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
                    <strong>{{ $t('infrastructure.actions') }}</strong>
                  </v-col>
                  <template v-if="infrastructureType === 'point'">
                    <v-col cols="12" md="3">
                      <v-checkbox v-model="diagData.isolation_advice" :label="$t('infrastructure.toInsulate')"
                        density="compact" />
                    </v-col>
                    <v-col cols="12" md="3">
                      <v-checkbox v-model="diagData.dissuasion_advice" :label="$t('infrastructure.discourage')"
                        density="compact" />
                    </v-col>
                    <v-col cols="12" md="3">
                      <v-checkbox v-model="diagData.attraction_advice" :label="$t('infrastructure.providingIncentives')"
                        density="compact" />
                    </v-col>
                    <v-col cols="12" md="3">
                      <v-checkbox v-model="diagData.change_advice" :label="$t('infrastructure.changeAdvice')"
                        density="compact" />
                    </v-col>
                  </template>
                  <template v-if="infrastructureType === 'line'">

                    <v-col cols="12" md="6">
                      <v-checkbox v-model="diagData.visibility_advice"
                        :label="$t('infrastructure.visibilityAdvice')"
                        density="compact" />
                    </v-col>
                    <v-col cols="12" md="6">
                      <v-checkbox v-model="diagData.burial_advice" :label="$t('infrastructure.burialAdvice')"
                        density="compact" />
                    </v-col>

                  </template>
                  <v-col cols="12" class="text-left">
                    <v-textarea v-model="diagData.technical_proposal" clearable clear-icon="mdi-close-circle"
                      :label="$t('infrastructure.technicalProposal')" :rules="[rules.textLength]" rows="2" counter="300"
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
import type { DiagData, Diagnosis } from '~/types/cables';
import type { NomenclatureItem } from '~/types/nomenclature';
import type { NotificationInfo } from '~/types/notifications';
import * as errorCodes from '~/static/errorConfig.json';
import { getLocaleDateString } from '~/helpers/formHelpers';
import { generateSnackbarMessage } from '~/helpers/messageHelpers';

const { t } = useI18n()
const router = useRouter()
const route = useRoute()

const cablesStore = useCablesStore()
const nomenclaturesStore = useNomenclaturesStore()
const notificationStore = useNotificationStore()
const mediaStore = useMediaStore()

const formValid = ref(false)
const infrastructureId = computed(() => cablesStore.formInfrastructureId)
const formInfrastructure = computed(() => cablesStore.formInfrastructure)
const infrastructureType = computed(() => route.query.type && typeof route.query.type == 'string' ? (route.query.type).toLowerCase() : '')
const networkTypeId = computed<number>(() => parseInt(route.query.network_type as string) || formInfrastructure.value?.properties?.network_type?.id || 0);
const diagnosisReady = ref(false)
const diagnosisId = computed(() => route.query.id_diagnosis)
const armingItems = computed(() => nomenclaturesStore.getArmingItems(infrastructureType.value, networkTypeId.value))


const diagData: DiagData = reactive({
  // date: new Date(Date.now() - new Date().getTimezoneOffset() * 60000),
  date: getLocaleDateString(new Date()),
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
  burial_advice: false,
  visibility_advice: false,
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
    const diagnosis = await api.get<Diagnosis>(`/api/v1/cables/diagnosis/${diagnosisId.value}/`)
    if (diagnosis) {
      const date = diagnosis.date ? new Date(diagnosis.date) : null
      if (date) {
        cablesStore.setFormDate(date)
        console.debug(date)
      }
      // mediaStore.date = formDate.value
      mediaStore.medias = diagnosis.media
      const diagdata: DiagData = {
        id: diagnosis.id,
        date: getLocaleDateString(cablesStore.getFormDate),
        remark: diagnosis.remark,
        technical_proposal: diagnosis.technical_proposal,
        infrastructure: diagnosis.infrastructure,
        arming_id: diagnosis.arming?.map((item: NomenclatureItem) => item.id),
        neutralized: diagnosis.neutralized,
        condition_id: diagnosis.condition?.id,

        visibility_advice: diagnosis.visibility_advice,
        media_id: [],
      }
      if (infrastructureType.value === 'point') {
        diagdata.attraction_advice = diagnosis.attraction_advice
        diagdata.dissuasion_advice = diagnosis.dissuasion_advice
        diagdata.isolation_advice = diagnosis.isolation_advice
        diagdata.pole_attractivity_id = diagnosis.pole_attractivity?.id
        diagdata.pole_dangerousness_id = diagnosis.pole_dangerousness?.id
      }
      if (infrastructureType.value === "line") {
        diagdata.change_advice = diagnosis.change_advice
        diagdata.burial_advice= diagnosis.burial_advice
        diagdata.sgmt_moving_risk_id = diagnosis.sgmt_moving_risk?.id
        diagdata.sgmt_topo_integr_risk_id = diagnosis.sgmt_topo_integr_risk?.id
        diagdata.sgmt_landscape_integr_risk_id = diagnosis.sgmt_landscape_integr_risk?.id
      }
      Object.assign(diagData, diagdata)
      diagnosisReady.value = true
    }
  }
  // } else if (!cablesStore.getFormDate) {
  //   cablesStore.setFormDate(new Date())
  // }
  // const diagData = null
}

watch(() => cablesStore.getFormDate, (newDate) => {
  diagData.date = getLocaleDateString(newDate)
})

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
    console.debug('diagData', diagData)
    diagData.media_id = await createMedias()
    const url = diagData.id ? `/api/v1/cables/diagnosis/${diagData.id}/` : '/api/v1/cables/diagnosis/'
    const diagnosis = diagData.id ? await api.put(url, diagData) : api.post(url, diagData)
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
  try {
    const diagnosis = await createDiagnosis()
    if (diagnosis) {
      router.push(`/infrastructures/${infrastructureId.value}`)
    }
  } catch (err) {
    const error: NotificationInfo = {
      type: 'error',
      msg: `${t(`error.${errorCodes.create_point.msg}`)} - ${err}`
    }
    notificationStore.setInfo(error)
  }
};

onMounted(() => {
  initData()
})

onUnmounted(() => {
  mediaStore.resetMedias()
})

</script>
