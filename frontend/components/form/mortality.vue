<template>
  <v-layout full-height>
    <v-app-bar color="pink" flat dark density="compact">
      <template #prepend>
        <v-btn icon="mdi-pencil-circle" />
        <v-app-bar-title>{{ modifyDiag ? 'Modifier le' : 'Nouveau' }}
          {{ $t('mortality.new_mortality') }}
        </v-app-bar-title>
      </template>
      <template #append>
        <v-btn icon="mdi-close" @click="router.back()" />
      </template>
    </v-app-bar>

    <v-main scrollable>
      <v-form ref="form" v-model="formValid" class="text-center">
        <v-card-text class="overflow-auto">
          <v-container>
            <v-row>
              <v-col cols="12" class="text-left">
                <strong>{{ $t('forms.general') }}</strong>
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="12" md="6">
                <v-menu :close-on-content-click="false" transition="scale-transition">
                  <template #activator="{ props }">
                    <v-text-field v-model="mortalityData.date" :label="$t('forms.datecreate')" persistent-hint
                      prepend-icon="mdi-calendar" variant="solo" density="compact" v-bind="props" />
                  </template>
                  <v-date-picker v-model="mortalityData.date" no-title />
                </v-menu>
              </v-col>

              <v-col cols="12" md="6">
                <v-autocomplete v-model="mortalityData.species_id" v-model:search="speciesSearch" :loading="isLoading"
                  :items="specieSearchEntries" item-title="vernacular_name" item-value="id" label="Espèce"
                  auto-select-first :rules="[rules.required]" required variant="solo" density="compact" hide-no-data
                  hide-details :placeholder="$t('Start typing to Search')" />
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field ref="author" v-model="mortalityData.author" :label="$t('mortality.observer')"
                  type="string" :placeholder="$t('mortality.observer')" hide-spin-buttons :rules="[rules.required]"
                  required variant="solo" density="compact" />
              </v-col>
              <v-col cols="12" md="6">
                <v-select v-model="mortalityData.death_cause_id" :items="nomenclaturesStore.deathCauseItems"
                  item-title="label" item-value="id" :rules="[rules.required]" required label="Cause de la mortalité"
                  variant="solo" density="compact" />
              </v-col>
              <v-col cols="12">
                <v-text-field ref="infrstr"
                  :value="mortalityInfrastructure?.properties ? `#${mortalityInfrastructure?.properties.id} ${mortalityInfrastructure?.resourcetype} ${mortalityInfrastructure?.properties.owner.label}` : ''"
                  label="support/ligne concerné" type="string" placeholder="support/ligne concerné" hide-spin-buttons
                  variant="solo" density="compact" readonly focused :messages="t('Cliquez sur la carte')">
                  <template #append>
                    <v-btn color="info" :disabled="mortalityGetInfrastructure"
                      @click="mortalityGetInfrastructure = !mortalityGetInfrastructure">{{ t('attachInfrastructure') }}</v-btn>
                  </template>
                </v-text-field>
              </v-col>
              <v-col cols="12">
                <v-text-field v-model="mortalityData.data_source_url" clearable clear-icon="mdi-close-circle"
                  :label="$t('mortality.dataSourceUrl')" :rules="[rules.urlRules]" variant="solo" density="compact" />
              </v-col>
              <v-col cols="12">
                <v-textarea v-model="mortalityData.comment" clearable clear-icon="mdi-close-circle"
                  :label="$t('remark')" :rules="[rules.textLength]" rows="2" counter="300" variant="solo"
                  density="compact" />
              </v-col>
            </v-row>
          </v-container>

          <v-divider />
          <v-container>
            <v-row>
              <v-col cols="12" class="text-left">
                <strong>{{ $t('picture.pictures') }}</strong>
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="12">
                <!-- <utils-picture-component ref="upc" :loaded-images="loadedImages" /> -->
                <form-images :medias="mortalityData.media" @update="getFormMedias"></form-images>
              </v-col>
              in parent
              <pre><code>{{ loadedImages }}</code></pre>
            </v-row>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-row class="justify-space-around mb-2">
            <v-btn color="red" variant="elevated" prepend-icon="mdi-close" @click="back">{{ $t('app.cancel')
              }}</v-btn>
            <v-btn color="green" :disabled="!(formValid && !!mortalityData.geom)" variant="elevated"
              prepend-icon="mdi-check" @click="submit">{{
                $t('app.valid')
              }}</v-btn>
          </v-row>
        </v-card-actions>
      </v-form>
      <!-- <pre><code>{{ mortalityData }}</code></pre> -->
    </v-main>
  </v-layout>
</template>

<script setup lang="ts">
import { storeToRefs } from 'pinia'
import * as errorCodes from '~/static/errorConfig.json'
import type { NotificationInfo } from '~/types/notifications'

const { mortality } = defineProps(['mortality'])
const { t } = useI18n()
const router = useRouter()
const notificationStore = useNotificationStore()
const coordinatesStore = useCoordinatesStore()
const nomenclaturesStore = useNomenclaturesStore()
// Species Autocomplete data
const descriptionLimit = ref(60)
const isLoading = ref(false)
const speciesSearch = ref(null)
const specieSearchEntries = ref([])
const loadedImages = ref([])


const formValid = ref(true)

const mortalityData = reactive({
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

const { newGeoJSONObject, mortalityInfrastructure, mortalityGetInfrastructure } = storeToRefs(coordinatesStore)

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



const submit = async () => {
  if (formValid.value) {
    // Case of creation of new Point and associated Diagnosis
    if (!mortality) {
      await createNewData()
      // new Point is successfully created
    }
    router.push('/search#morality')
  }
}


const createNewData = async () => {
  try {
    mortalityData.geom = newGeoJSONObject.value?.geometry
    const { data } = await useApi('/api/v1/mortality/', { method: 'post', body: mortalityData })
    // await createNewMedia(data.value.id)
    console.debug(data.value)
    mortalityInfrastructure.value = {}
    mortalityGetInfrastructure.value = false
  } catch (_err) {
    console.error(_err)
    const error: NotificationInfo = {
      type: 'error',
      msg: t(`error.${errorCodes.create_point.msg}`)
    }
    notificationStore.setInfo(error)
    back()
  }
}


const createNewMedia = async (id) => {
  const mediaIdList = []
  // await all Promises be resolved before returning result
  await Promise.all(
    // upc for "util-picture-component": task on each img file of the map
    loadedImages.value.map(async (img) => {
      try {
        const formData = new FormData()
        console.log('img', img)
        formData.append('storage', img) // fill-in FormData with img file
        // TODO get true date and other form fields below
        formData.append('date', '2022-01-01')
        formData.append('author', 'Bob')
        formData.append('source', 'LPO')
        formData.append('remark', 'Nothing to report')
        console.log('formData', formData)
        // create Media
        const { data: newImg } = await useApi("/api/v1/media/", {
          method: 'POST',
          headers: {
            'Content-Type': 'multipart/form-data'
          },
          body: formData
        })
        console.log('newImg', newImg)
        mediaIdList.push(newImg.value.id) // set Media id to mediaIdList
      } catch (_err) {
        console.debug(_err)
        const error: NotificationInfo = {
          type: 'error',
          msg: t(`error.${errorCodes.create_point.msg}`)
        }
        notificationStore.setInfo(error)
        back()
      }
    })
  )
  console.log('mediaList', mediaIdList)
  await useApi(`/api/v1/mortality/${id}`, { method: 'put', body: { media: mediaIdList } })
}

</script>
