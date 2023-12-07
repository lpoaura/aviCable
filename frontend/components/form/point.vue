<template>
  <v-card elevation="0" class="fill-height">
    <v-layout full-height>
      <v-form ref="form" v-model="formValid" class="fill-height text-center">
        <v-app-bar color="pink" flat dark density="compact">
          <template v-slot:prepend>
            <v-btn icon="mdi-pencil"></v-btn>
            <v-app-bar-title>{{ modifyDiag ? 'Modifier le' : 'Nouveau' }}
              {{ diagnosis ? 'diagnostic' : $t('support.support') }}
            </v-app-bar-title>
          </template>
          <template v-slot:append>
            <v-btn icon="mdi-close" @click="router.back()" />
          </template>
        </v-app-bar>
        <v-main scrollable>
          <v-card-text>
            <v-container v-if="!(diagnosis || support)">
              <v-row>
                <v-col cols="12" class="text-left">
                  <strong> {{ $t('forms.general-infrastructure') }}</strong>
                </v-col>
              </v-row>
              <v-row>
                <v-col cols="12" md="4">
                  <v-text-field ref="lat" v-model="coordinatesStore.newGeoJSONPoint.coordinates[1]"
                    :label="$t('support.latitude')" type="number" placeholder="Latitude"
                    :rules="[rules.requiredOrNotValid, rules.latRange]" required variant="solo" density="compact" />
                </v-col>

                <v-col cols="12" md="4">
                  <v-text-field ref="lng" v-model="coordinatesStore.newGeoJSONPoint.coordinates[0]"
                    :label="$t('support.longitude')" type="number" placeholder="Longitude"
                    :rules="[rules.requiredOrNotValid, rules.lngRange]" required variant="solo" density="compact" />
                </v-col>
                <v-col cols="12" md="4" v-if="!diagnosis">
                  <v-select v-model="pointData.owner_id" :items="networkOwners" item-title="label" item-value="id"
                    :rules="[rules.required]" :label="$t('support.network')" variant="solo" density="compact" required>
                  </v-select>
                </v-col>
              </v-row>
            </v-container>
            <v-divider v-if="!(diagnosis || support)"></v-divider>
            <v-container>
              <v-row>
                <v-col cols="12" class="text-left">
                  <h2>{{ $t('display.diagnosis') }}</h2>
                </v-col>
              </v-row>
              <v-row>
                <!--
                   <p>pointData
                <pre><code>{{ pointData }}</code></pre>
                </p>
                <p>support
                <pre><code>{{ support}}</code></pre>
                </p>

                <p>diagnosis
                <pre><code>{{ diagnosis }}</code></pre>
                </p>
                <p>diagData
                <pre><code>{{ diagData }}</code></pre>
                </p>-->
                <v-col cols="12" md="4">
                  <v-menu>

                    <template v-slot:activator="{ props }">
                      <v-text-field v-model="diagData.date" :label="$t('forms.datecreate')" persistent-hint
                        inner-prepend-icon="mdi-calendar" variant="solo" density="compact" v-bind="props" />
                    </template>
                    <v-date-picker v-model="diagData.date" no-title></v-date-picker>
                  </v-menu>
                </v-col>
                <v-col cols="12" md="4">
                  <v-select v-model="diagData.condition_id" :items="conditions" item-title="label" item-value="id"
                    :rules="[rules.required]" :label="$t('support.condition')" variant="solo"
                    density="compact"></v-select>
                </v-col>
                <!-- TODO: virer champ  Neutralisé pour remplacer par la présence d'équipement (oui/non) -->
                <v-col cols="12" md="4">
                  <v-checkbox v-model="diagData.neutralized" :label="$t('diagnosis.equipment')"
                    density="compact"></v-checkbox>
                </v-col>

                <v-col cols="12">
                  <v-autocomplete chips v-model="diagData.pole_type_id" :items="poleTypes" item-title="label"
                    item-value="id" :rules="[rules.required]" hide-selected :label="$t('support.support-type')" multiple
                    deletable-chips variant="solo" density="compact"></v-autocomplete>
                </v-col>
                <v-col cols="12" md="6">
                  <v-select v-model="diagData.pole_attractivity_id" :items="riskLevels" item-title="label" item-value="id"
                    :rules="[rules.required]" :label="$t('support.attractiveness')" variant="solo"
                    density="compact"></v-select>
                </v-col>
                <v-col cols="12" md="6">
                  <v-select v-model="diagData.pole_dangerousness_id" :items="riskLevels" item-title="label"
                    item-value="id" :rules="[rules.required]" :label="$t('support.dangerousness')" variant="solo"
                    density="compact"></v-select>
                </v-col>
                <v-divider></v-divider>
                <v-col cols="12" class="text-left">
                  <strong>{{$t('diagnosis.actions')}}</strong>
                </v-col>


                <v-col cols="12" md="3">
                  <v-checkbox v-model="diagData.isolation_advice" :label="$t('support.advice_isol')"
                    density="compact"></v-checkbox>
                </v-col>
                <v-col cols="12" md="3">
                  <v-checkbox v-model="diagData.dissuasion_advice" :label="$t('support.advice_disrupt')"
                    density="compact"></v-checkbox>
                </v-col>

                <v-col cols="12" md="3">
                  <v-checkbox v-model="diagData.attraction_advice" :label="$t('support.advice_attract')"
                    density="compact"></v-checkbox>
                </v-col>
                <v-col cols="12" md="3">
                  <v-checkbox v-model="diagData.change_advice" :label="$t('support.change_advice')"
                    density="compact"></v-checkbox>
                </v-col>
                <v-col cols="12" class="text-left">
                  <v-textarea v-model="diagData.technical_proposal" clearable clear-icon="mdi-close-circle"
                    :label="$t('diagnosis.technical_proposal')" :rules="[rules.textLength]" rows="2" counter="300"
                    variant="solo" density="compact"></v-textarea>
                </v-col>
                <v-divider></v-divider>
                <v-col cols="12">
                  <v-textarea v-model="diagData.remark" clearable clear-icon="mdi-close-circle" :label="$t('app.remark')"
                    :rules="[rules.textLength]" rows="2" counter="300" variant="solo" density="compact"></v-textarea>
                </v-col>
              </v-row>
            </v-container>
            <v-container>
              <v-row>
                <v-col cols="12" class="text-left">
                  <h2>{{ $t('display.equipments') }}</h2>
                </v-col>
              </v-row>
              <v-row>
              </v-row>
            </v-container>
            <v-divider></v-divider>
            <v-container>
              <v-row>
                <v-col cols="12" class="text-left">
                  <strong>{{ $t('picture.pictures') }}</strong>
                </v-col>
              </v-row>
              <v-row>
                <v-col cols="12">
                  <utils-picture-component ref="upc" />
                </v-col>
                <v-container>
                  <v-list v-if="diagnosis && modifyDiag">
                    <v-list-item v-for="img in diagnosis.media" :key="img.id">
                      <v-row>
                        <v-col>
                          <v-img :src="img.storage" max-height="100" max-width="166" class="ma-2" />
                        </v-col>
                        <v-col></v-col>
                        <v-col cols="1">
                          <v-icon small color="red">mdi-trash-can</v-icon>
                        </v-col>
                      </v-row>
                    </v-list-item>
                  </v-list>
                </v-container>
              </v-row>
            </v-container>
          </v-card-text>
          <v-card-actions>
            <v-row class="justify-space-around mb-2">
              <v-btn color="red" variant="elevated" prepend-icon="mdi-close" @click="back">{{ $t('app.cancel')
                }}</v-btn>
              <v-btn color="green" :disabled="!formValid" variant="elevated" prepend-icon="mdi-check" @click="submit">{{
                $t('app.valid')
                }}</v-btn>
            </v-row>
          </v-card-actions>
          <pre>{{ support }}</pre>
        </v-main>
      </v-form>

    </v-layout>
  </v-card>
</template>
<script setup lang="ts">
import * as errorCodes from '~/static/errorConfig.json'
import type { ErrorInfo } from '~/store/errorStore';

// init modules
const {t} = useI18n()
const router = useRouter()
const route = useRoute()

// init Stores
const coordinatesStore = useCoordinatesStore()
const nomenclaturesStore = useNomenclaturesStore()
const errorStore = useErrorsStore()

// props
//const {support, diagnosis, operation} = defineProps(['support', 'diagnosis', 'operation'])
const {support, diagnosis, operation}  = defineProps<{
  support?: Object,
  diagnosis?: Diagnosis,
}>()

const upc = ref(null)
// data
const form = ref(null) // used to get form ref from "<v-form ref="form">"
const formValid = ref(true)
// manualChange: false, // boolean to activate manual coordinate change
// form values
const lat: Ref<null | number> = ref<null | number>(0)
const lng: Ref<null | number> = ref<null | number>(null)
// To manage Media
const newCreatedMediaIdList: Array<object> = reactive([])
// define data related to Point
const pointData = reactive({
  geom: coordinatesStore.newGeoJSONPoint,
  owner_id: support ? support.owner_id : null,
})
// define data related to Diagnosis

const modifyDiag = computed(() => route.query.modifyDiag === 'true' ? true : false)
const diagnosisId = computed(() => route.query.id_diagnosis)

const diagData : DiagData = reactive({
  date: new Date(Date.now() - new Date().getTimezoneOffset() * 60000)
              .toISOString().substr(0, 10),
  remark: null,
  infrastructure:null,
  pole_type_id: [],
  neutralized: false,
  condition_id: null,
  attraction_advice:false,
  dissuasion_advice: false,
  isolation_advice: false,
  pole_attractivity_id: null,
  pole_dangerousness_id: null,
  media_id: [],
})

//       // rules for form validation
const rules = reactive({
  required: (v: string | number) => !!v || t('valid.required'),
  requiredOrNotValid: (v: string | number) => v === 0 || !!v || t('valid.required_or_not_valid'),
  latRange: (v: number) => (v >= 40 && v <= 52) || `${t('valid.range')}40 : 52`,
  lngRange: (v: number) => (v >= -20 && v <= 20) || `${t('valid.range')}-20 : 20`,
  textLength: (v: string) => (v || '').length <= 300 || `${t('valid.length')}: 300`,
})


// Menu items
const poleTypes = computed(() => nomenclaturesStore.poleTypeItems)
const networkOwners = computed(() => nomenclaturesStore.ownerItems)
const conditions = computed(() => nomenclaturesStore.conditionItems)
const riskLevels = computed(() => nomenclaturesStore.riskLevelItems)


// Methods
const back = () => {
  coordinatesStore.setNewGeoJSONPoint({coordinates: [], type: 'Point'})
  router.back()
}

/**
 * submit(): Method to submit the form for Point/Diagnosis/Media creation or update
 * .
 *
 * If process fail at any step, all elements created before are deleted through error handling
 * process.
 */

const initData = async() => {
  if (support && diagnosisId) {}
  // const diagData = null
}

const submit = async () => {
  console.debug('formValid', formValid.value)
  console.debug('hasSupport', support ? 'Oui': 'Non')
  console.debug('hasDiag', diagnosis ? 'Oui': 'Non')
  console.debug('hasModifyDiag', modifyDiag ? 'Oui': 'Non')
  console.debug('hasModifyDiag.value', modifyDiag.value ? 'Oui': 'Non')
  if (formValid.value) {
    console.log('SUPPORT & DIAGNOSIS', support, diagnosis)
    // Case of creation of new Point and associated Diagnosis
    if (!support && !diagnosis) {
      console.debug('createNewPoint !support && !diagnosis')
      const pointCreated = await createNewPoint()
      console.debug(pointCreated)
      // new Point (Support) is successfully created
      if (pointCreated) {
        // Create Diagnosis
        await createNewDiagnosis(pointCreated.properties.id)
      }
      router.push('/search')
    } else if (diagnosis && modifyDiag) {
      console.debug('updateDiagnosis diagnosis && modifyDiag')
      // Case of update of Diagnosis
      await updateDiagnosis()
      router.push(`/supports/${diagnosis.infrastructure}`)
    } else if (support && !diagnosis && !modifyDiag.value) {
      // Case of creation of new Diagnosis on existing Support
      console.debug('addNewDiagnosis diagnosis && !modifyDiag')
      const data = await addNewDiagnosis()
      console.debug('DIAG', data)
      router.push(`/supports/${data?.value.infrastructure}`)
    } else {
      console.debug('else ERROR')
      // update of existing Point
      const error = {
        code: 0,
        msg: 'Update of Support not implemented yet',
      }
      // set error message to errorStore and triggers message display through "err"
      // watcher in error-snackbar component
      // this.$store.commit('errorStore/setError', error)
    }
  }
}

/**
 * createNewPoint(): Method that create new Point based on forms data (cf. this.pointData)
 *
 * @return {JSON object} as new Point
 *
 * If process fails, error message is displayed in snackBar through error handling process.
 */
const createNewPoint = async () => {
  try {
    pointData.geom = coordinatesStore.newGeoJSONPoint
    const {data} = await useHttp('/api/v1/cables/points/', {method: 'post', body: pointData})
    console.debug('createNewPoint', data.value)
    return data.value
  } catch (_err) {
    const error : ErrorInfo = {
      code:errorCodes.create_point.code,
      msg:t(`error.${errorCodes.create_point.msg}`)
    }
    errorStore.setError(error )
    // error.code = errorCodes.create_point.code
    // error.msg = t(`error.${errorCodes.create_point.msg}`)
    // set error message to errorStore and triggers message display through "err" watcher in
    // error-snackbar component
    // errorStore.setError(error)
    back()
  }
}

/**
 * createNewDiagnosis(): Method that create new Diagnosis based on forms data(cf.this.diagData)
 *
 * @param {Number} infrstr_id id of related Insfrastructure (Point)
 *
 * Error handling: A Diagnosis should be created at time of Infrastructure (Point) creation.
 * If Diagnosis creation fails, related Infrastructure (Point) will be deleted.
 * Related Media will also be deleted in this case.
 * Finally, error message is displayed in snackBar through error handling process.
 */
const createNewDiagnosis = async (infrstr_id: number) => {
  // Create Media as selected in component form and get list of Ids of created Media
  // const mediaIdList = await createNewMedia()
  try {
    diagData.infrastructure = infrstr_id // set Infrastructure (Point) id
    // diagData.media_id = mediaIdList // set Media id list
    const {data} = await useHttp('/api/v1/cables/diagnosis/', {method: 'post', body: diagData})
    return data.value
  } catch (_err) {
    // If Diagnosis creation fails, related infrastructure(Point) is deleted
    await useHttp(`/api/v1/cables/points/${infrstr_id}/`, {method: 'delete'})
    // If Diagnosis creation fails, related Media created are deleted
    if (newCreatedMediaIdList) {
      newCreatedMediaIdList.forEach(
          async (media_id) => await useHttp(`/api/v1/media/${media_id}/`, {method: 'delete'})
      )
    }
    // Error display
    const error = {}
    // error.code = errorCodes.create_pole_diagnosis.code
    // error.msg = $nuxt.$t(`error.${errorCodes.create_pole_diagnosis.msg}`)
    // // set error message to errorStore and triggers message display through "err" watcher / in error-snackbar component
    // this.$store.commit('errorStore/setError', error)
    back()
  }
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
const addNewDiagnosis = async () => {
  // Create Media as selected in component form and get list of Ids of created Media
  console.debug('modifyDiag', modifyDiag ? 'vrai' : 'faux')
  console.debug(diagData, )
  // const mediaIdList = await createNewMedia()
  try {
    console.debug('support', support.value.properties)
    diagData.infrastructure = support.value.properties.id // set Infrastructure (Point) id
    // diagData.media_id = mediaIdList // set Media id list
    // Create Diagnosis
    const {data }= await useHttp('/api/v1/cables/diagnosis/', {method:'post', body: diagData})
    console.debug('newDiagData', data)
    return data
  } catch (_err) {
    console.error ('error',_err)
    // If Diagnosis creation fails, related Media created are deleted
    // if (newCreatedMediaIdList) {
    //   newCreatedMediaIdList.forEach(
    //       async (media_id) => await this.$axios.$delete(`/media/${media_id}/`)
    //   )
    // }
    // Error display
    const error : ErrorInfo = {code : errorCodes.create_pole_diagnosis.code,msg :t(`error.${errorCodes.create_pole_diagnosis.msg}`)}
    errorStore.setError(error)
    back()
  }
}

/**
 * updateDiagnosis(): Method that update Diagnosis based on forms data (cf.this.diagData)
 *
 * Error handling: If Diagnosis update fails, new created Media will be deleted.
 * Finally, error message is displayed in snackBar through error handling process.
 */
const updateDiagnosis = async () => {
  // Create new Media as selected in component form and get list of Ids of created Media
  const mediaIdList = await this.createNewMedia()
  try {
    this.diagData.infrastructure = diagnosis.infrastructure // set Infrastructure (Point) id
    this.diagData.media_id = mediaIdList // set Media id list
    // Create Diagnosis
    return await this.$axios.$put(
        `cables/diagnosis/${diagnosis.id}/`,
        this.diagData
    )
  } catch (_err) {
    // If Diagnosis creation fails, related Media created are deleted
    if (this.newCreatedMediaIdList) {
      this.newCreatedMediaIdList.forEach(
          async (media_id) => await this.$axios.$delete(`/media/${media_id}/`)
      )
    }
    // Error display
    const error = {}
    error.code = errorCodes.update_pole_diagnosis.code
    error.msg = $nuxt.$t(`error.${errorCodes.update_pole_diagnosis.msg}`)
    // set error message to errorStore and triggers message display through "err" watcher / in error-snackbar component
    this.$store.commit('errorStore/setError', error)
    this.back()
  }
}

/**
 * createNewMedia(): Method that create new Media based on component forms data and return the
 * list of Ids of created Media
 *
 * @return {Number[]} as new Diagnosis
 *
 * If process fails for at least one Media creation, error message is displayed in snackBar
 * through error handling process. Id of Media for which creation did not fail will be return
 * anyway.
 */
const createNewMedia = async () => {
  const mediaIdList = modifyDiag ? diagData.media_id : []
  console.debug('upc',upc.value)
  // await all Promises be resolved before returning result
  await Promise.all(
      // upc for "util-picture-component": task on each img file of the map
      upc.imgFileObject.map(async (img) => {
        try {
          const formData = new FormData()
          formData.append('storage', img) // fill-in FormData with img file
          // TODO get true date and other form fields below
          formData.append('date', '2022-01-01')
          formData.append('author', 'Bob')
          formData.append('source', 'LPO')
          formData.append('remark', 'Nothing to report')
          // create Media
          const options = {
            headers: {
              accept: 'application/json',
              'Content-Type': 'multipart/form-data',
            },
            method: "post",
          }
          const {data} = await useHttp('/api/v1/cables/points/', {method: 'post', body: formData})

          mediaIdList.push(data.value.id) // set Media id to mediaIdList
          newCreatedMediaIdList.push(data.value.id)
        } catch (_err) {
          const error = {}
          // error.code = errorCodes.img_sending.code
          // error.msg = $nuxt.$t(`error.${errorCodes.img_sending.msg}`)
          // // set error message to errorStore and triggers message display through "err"
          // // watcher in error-snackbar component
          // this.$store.commit('errorStore/setError', error)
        }
      })
  )
  return mediaIdList
}

// onMounted(() => {
//   console.log('WATCH DIAG', diagnosis ? 'Oui':'Non')
//   console.log('DIAGNOSIS TEST', diagnosis)
//   if (diagnosis) {
//     console.log('diagnosis.neutralized ',diagnosis )
//     console.log('WATCH UPDATE DIAGDATA')
//     diagData.value = {
//       date: diagnosis.date,
//       remark: diagnosis.remark,
//       infrastructure: diagnosis.infrastructure ,
//       pole_type_id: diagnosis.pole_type.map((pt) => pt.id),
//       neutralized: diagnosis.neutralized ,
//       condition_id: diagnosis.condition.id,
//       attraction_advice: diagnosis.attraction_advice,
//       dissuasion_advice: diagnosis.dissuasion_advice,
//       isolation_advice: diagnosis.isolation_advice,
//       pole_attractivity_id: diagnosis.pole_attractivity.id,
//       pole_dangerousness_id: diagnosis.pole_dangerousness.id,
//       media_id: diagnosis.media.map((m) => m.id)
//     }
//   }
//   console.log('WATCH DIAG diagData after' , diagData)
// })


</script>
<style>
.required label::after {
  content: "*";
}
</style>
