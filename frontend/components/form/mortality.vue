<template>
  <v-card elevation="0" class="fill-height">
    <v-form ref="form" v-model="formValid">
      <v-card-text>
        <v-row>
          <v-container>
            <v-card title="Infos" prepend-icon="mdi-information">
              <v-container>
                <v-row>
                  <v-col cols="12" class="text-left">
                    <strong>{{ $t('forms.general') }}</strong>
                  </v-col>
                  <v-col cols="12" md="6">
                    <v-date-input v-model="formDate" label="Date de visite" inner-prepend-icon="mdi-calendar"
                      variant="solo" density="compact" :rules="[rules.required]" :max="new Date()" />
                  </v-col>
                  <v-col cols="12" md="6">
                    <v-autocomplete v-model="mortalityData.species_id" v-model:search="speciesSearch"
                      :loading="isLoading" :items="specieSearchEntries" item-title="vernacular_name" item-value="id"
                      label="Espèce" auto-select-first :rules="[rules.required]" required variant="solo"
                      density="compact" hide-no-data hide-details :placeholder="$t('Start typing to Search')" />
                  </v-col>
                  <v-col cols="12" md="6">
                    <v-text-field ref="author" v-model="mortalityData.author" :label="$t('mortality.observer')"
                      type="string" :placeholder="$t('mortality.observer')" hide-spin-buttons :rules="[rules.required]"
                      required variant="solo" density="compact" />
                  </v-col>
                  <v-col cols="12" md="6">
                    <v-select v-model="mortalityData.death_cause_id" :items="nomenclaturesStore.deathCauseItems"
                      item-title="label" item-value="id" :rules="[rules.required]" required
                      label="Cause de la mortalité" variant="solo" density="compact" />
                  </v-col>
                  <v-col cols="12">
                    <v-text-field ref="infrstr"
                      :value="mortalityInfrastructure?.properties ? `#${mortalityInfrastructure?.properties.id} ${mortalityInfrastructure?.resourcetype} ${mortalityInfrastructure?.properties.owner.label}` : ''"
                      label="support/ligne concerné" type="string" placeholder="support/ligne concerné"
                      hide-spin-buttons variant="solo" density="compact" readonly focused
                      :messages="t('Cliquez sur la carte')">
                      <template #append>
                        <v-btn color="info" :disabled="mortalityGetInfrastructure"
                          @click="mortalityGetInfrastructure = !mortalityGetInfrastructure">{{ t('attachInfrastructure')
                          }}</v-btn>
                      </template>
                    </v-text-field>
                  </v-col>
                  <v-col cols="12">
                    <v-text-field v-model="mortalityData.data_source_url" clearable clear-icon="mdi-close-circle"
                      :label="$t('mortality.dataSourceUrl')" :rules="[rules.urlRules]" variant="solo"
                      density="compact" />
                  </v-col>
                  <v-col cols="12">
                    <v-textarea v-model="mortalityData.comment" clearable clear-icon="mdi-close-circle"
                      :label="$t('remark')" :rules="[rules.textLength]" rows="2" counter="300" variant="solo"
                      density="compact" />
                  </v-col>
                </v-row>
              </v-container>
            </v-card>
          </v-container>
        </v-row>
        <form-images :medias="mortalityData.media"></form-images>
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn color="green" :disabled="!(formValid && !!mortalityData.geom)" variant="flat"
          prepend-icon="mdi-content-save-all" @click="submit">{{
            $t('app.valid')
          }}</v-btn>
      </v-card-actions>
    </v-form>
    <!-- <pre><code>{{ mortalityData }}</code></pre> -->
  </v-card>
</template>

<script setup lang="ts">
import { storeToRefs } from 'pinia'
import type { MortalityFeature, Mortality } from '~/types/mortality'
import type { NotificationInfo } from '~/types/notifications'

// const { mortality } = defineProps(['mortality'])
const { t } = useI18n()
const router = useRouter()
const route = useRoute()

const notificationStore = useNotificationStore()
const coordinatesStore = useCoordinatesStore()
const nomenclaturesStore = useNomenclaturesStore()
// Species Autocomplete data


const descriptionLimit = ref(60)
const mediaStore = useMediaStore()
const isLoading = ref(false)
const speciesSearch = ref(null)
const specieSearchEntries = ref([])


const formValid = ref(true)
const formDate = ref(new Date(Date.now() - new Date().getTimezoneOffset() * 60000))

const mortalityId = computed(() => route.query.id_mortality)

const mortalityData = reactive<Mortality>({
  date: new Date(Date.now() - new Date().getTimezoneOffset() * 60000)
    .toISOString()
    .substr(0, 10),
  author: null,
  species_id: null, // null,
  infrstr_id: null,
  nb_death: 1,
  death_cause_id: null,
  data_source: null,
  data_source_url: null,
  comment: null,
  geom: null,
})

// rules for form validation
const rules = reactive({
  required: (v: string | number) => !!v || t('valid.required'),
  requiredOrNotValid: (v: string | number) => v === 0 || !!v || t('valid.required_or_not_valid'),
  latRange: (v: number) => (v >= 40 && v <= 52) || `${t('valid.range')}40 : 52`,
  lngRange: (v: number) => (v >= -20 && v <= 20) || `${t('valid.range')}-20 : 20`,
  textLength: (v: string) => (v || '').length <= 300 || `${t('valid.length')}: 300`,
  urlRules: (v: string) => !v || /^(ftp|http|https):\/\/[^ "]+$/.test(v) || 'Must be a valid URL (http://, https://, ftp://)',
})

const { newGeoJSONObject, mortalityInfrastructure, mortalityGetInfrastructure, selectedFeature } = storeToRefs(coordinatesStore)

watch(formDate.value, (newVal, _oldVal) => mediaStore.date = newVal)

watch(mortalityInfrastructure, (val) => {
  if (val) {
    mortalityData.infrstr_id = mortalityInfrastructure.value.properties.id
  }
})

watch(newGeoJSONObject, (val) => {
  if (val) {
    mortalityData.geom = newGeoJSONObject.value.geometry
  }
})


watch(speciesSearch, async (val) => {
  val && val !== mortalityData.species_id && speciesSelection(val)
})

const speciesSelection = async (value: string) => {
  isLoading.value = true
  const { data } = await useApi(`/api/v1/species/?search=${value}`)
  specieSearchEntries.value = data.value
  isLoading.value = false
}

const back = () => {
  router.back()
}


const createData = async () => {
  try {
    mortalityData.date = formDate.value.toISOString().substring(0, 10) // set Infrastructure (Point) id
    mortalityData.media_id = await createMedias()
    const url = mortalityId.value? `/api/v1/mortality/${mortalityId.value}/` : '/api/v1/mortality/'
    const method = mortalityId.value ? 'put' : 'post'
    const { data, error } = await useApi<MortalityFeature>(url, { method: method, body: mortalityData })
    if (error.value) {
      notificationStore.setInfo({
        type: 'error',
        msg: `${error}`
      })
    } else {
      notificationStore.setInfo({
        type: 'success',
        msg: 'Donnée de mortalité créée'
      })
    }
    console.debug('newDiagData', data)
    mediaStore.resetMedias()
    return data
  } catch (err) {

    console.error('error', err)
    const error: NotificationInfo = {
      type: 'error',
      msg: `Echec à la création de la donnée de mortalité : ${err}}`
    }
    notificationStore.setInfo(error)
  }
}




const submit = async () => {
  const data = await createData()
  console.log('submit', data, data?.value)
  if (data?.value?.id) {
    router.push(`/mortality/${data.value.id}`)
  }
}


const initData = async () => {
  if (mortalityId.value) {
    const { data } = await useApi<MortalityFeature>(`/api/v1/mortality/${mortalityId.value}/`, { method: 'get' })
    if (data.value) {
      formDate.value = new Date(data.value.properties.date)
      mediaStore.date = formDate.value
      mediaStore.medias = data.value.properties.media
      const mortalitydata = {
        id: data.value.id,
        date: data.value.properties.date,
        author: data.value.properties.author,
        species_id: data.value.properties.species.id, // null,
        infrstr_id: data.value.properties.infrstr.id,
        nb_death: data.value.properties.nb_death,
        death_cause_id: data.value.properties.death_cause.id,
        data_source: data.value.properties.data_source,
        data_source_url: data.value.properties.data_source_url,
        comment: data.value.properties.comment,
        geom: data.value.geometry,
      }
      Object.assign(mortalityData, mortalitydata)
      selectedFeature.value = data.value
    }
  }
  // const opData = null
}

const createMedias = async () => {
  return mediaStore.postMedias()
  // const images = mediaStore.postMedias()
  // return images
}

onMounted(() => {
  initData()
})

</script>
