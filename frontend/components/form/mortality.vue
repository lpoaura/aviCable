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
        {{ formValid ? 'Oui':'Non' }}
        <v-card-text class="overflow-auto">
          <v-container>
            <v-row>
              <v-col cols="12" class="text-left">
                <strong>{{ $t('forms.coordinates') }}</strong>
              </v-col>
            </v-row>
          </v-container>
          <v-divider />
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
                  auto-select-first required variant="solo" density="compact" hide-no-data hide-details
                  :placeholder="$t('Start typing to Search')" />
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field ref="lat" v-model="mortalityData.author" :label="$t('mortality.observer')" type="string"
                  :placeholder="$t('mortality.observer')" hide-spin-buttons required variant="solo" density="compact" />
              </v-col>
              <v-col cols="12" md="6">
                <v-select v-model="mortalityData.death_cause_id" :items="nomenclaturesStore.deathCauseItems"
                  item-title="label" item-value="id" :rules="[rules.required]" label="Cause de la mortalité"
                  variant="solo" density="compact" />
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field ref="lat" v-model="mortalityData.infrstr" label="support/ligne concerné" type="string"
                  placeholder="support/ligne concerné" hide-spin-buttons variant="solo" density="compact" />
              </v-col>
              <v-col cols="12">
                <v-text-field v-model="mortalityData.data_source_url" clearable clear-icon="mdi-close-circle"
                  :label="$t('mortality.dataSourceUrl')" :rules="[rules.urlRules]" variant="solo" density="compact" />
              </v-col>
              <v-col cols="12">
                <v-textarea v-model="mortalityData.comment" clearable clear-icon="mdi-close-circle"
                  :label="$t('app.remark')" :rules="[rules.textLength]" rows="2" counter="300" variant="solo"
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
                <utils-picture-component ref="upc" :loaded-images="loadedImages" />
              </v-col>
              in parent {{ loadedImages }}
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
      </v-form>
    </v-main>
  </v-layout>
</template>

<script setup lang="ts">
import { mapState, storeToRefs } from 'pinia'
import * as errorCodes from '~/static/errorConfig.json'
import type { ErrorInfo } from '~/store/errorStore';

const {mortality} = defineProps(['mortality'])
const {t} = useI18n()
const router =useRouter()
const errorStore = useErrorsStore()
const coordinatesStore = useCoordinatesStore()
const nomenclaturesStore = useNomenclaturesStore()
// Species Autocomplete data
const descriptionLimit = ref(60)
const isLoading = ref(false)
const speciesSearch = ref(null)
const specieSearchEntries = ref([])
const loadedImages = ref([])



// const speciesStore = useSpeciesStore()

const formValid = ref(true)
      // manualChange: false, // boolean to activate manual coordinate change
      // form values

      // define data related to Point

      const mortalityData = reactive({
        date: new Date(Date.now() - new Date().getTimezoneOffset() * 60000)
          .toISOString()
          .substr(0, 10),
        author: null,
        species_id: null, // null,
        infrstr: null,
        nb_death: 1,
        death_cause_id: null,
        data_source: null,
        data_source_url: null,
        comment: null,
        geom: {
          type: 'Point' as string,
          coordinates: [] as number[],
        },
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

const {newGeoJSONObject} = storeToRefs(coordinatesStore)

// const speciesStore = useSpeciesStore()

// const speciesFields = computed(() => {
//       return mortalityData.species ? Object.keys(mortalityData.species).map((key) => {
//         return {
//           key: mortalityData.species?[key] || 'n/a'
//         }
//       }) : []
//     })

    // const speciesItems = computed(
    // () => {
    //   return specieSearchEntries.value.map((entry) => {
    //     const vernacular_name =
    //       entry.vernacular_name.length > descriptionLimit
    //         ? entry.vernacular_name.slice(0, descriptionLimit) + '...'
    //         : entry.vernacular_name

    //     return Object.assign({}, entry, { vernacular_name })
    //   })
    // })

    watch(speciesSearch , async (val) => {
      val && val !== mortalityData.species_id && speciesSelection(val)
      // Items have already been loaded
      // if (speciesItems.value.length > 0) return

      // // Items have already been requested
      // if (isLoading.value) return

      // isLoading.value = true

      // // Lazily load input items
      // await useHttp(`species/?search=${value}`)
      //   .then((data) => {
      //     specieSearchEntries.value = data
      //   })
      // // TODO Manage error
      //   .catch((err) => {
      //     console.error(err)
      //   })
      //   .finally(() => (isLoading.value = false))
    })

const speciesSelection = async (value: string) => {
        isLoading.value = true
        // Simulated ajax query
        const {data} = await useHttp(`/api/v1/species/?search=${value}`)
        specieSearchEntries.value = data.value
        isLoading.value = false
        // setTimeout(() => {
        //   this.items = this.states.filter(e => {
        //     return (e || '').toLowerCase().indexOf((v || '').toLowerCase()) > -1
        //   })
        //   this.loading = false
        // }, 500)
      }

const back = () => {
      // this.$store.commit('coordinatesStore/addPointCoord', {
      //   lat: null,
      //   lng: null,
      // })
      router.back()
    }



   const submit =  async () => {
      if (formValid.value) {
        // Case of creation of new Point and associated Diagnosis
        if (!mortality) {
          await createNewData()
          // new Point is successfully created
        }
        router.push('/search#morality')
      }
    }

    /**
     * createNewPoint(): Method that create new Point based on forms data (cf. this.pointData)
     *
     * @return {JSON object} as new Point
     *
     * If process fails, error message is displayed in snackBar through error handling process.
     */
    const createNewData= async () => {
      try {
        mortalityData.geom = newGeoJSONObject.value?.geometry
        return await useHttp('/api/v1/mortality/', {method: 'post', body: mortalityData})
      } catch (_err) {
        console.error(_err)
        const error: ErrorInfo = {
          code : errorCodes.create_point.code,
          msg : t(`error.${errorCodes.create_point.msg}`)
        }
        errorStore.setError(error)
        back()
      }
    }

    /**
     * createNewDiagnosis(): Method that create new Diagnosis based on forms data(cf.this.mortalityData)
     *
     * @param {BigInt} infrstr_id id of related Insfrastructure (Point)
     *
     * Error handling: A Diagnosis should be created at time of Infrastructure (Point) creation.
     * If Diagnosis creation fails, related Infrastructure (Point) will be deleted.
     * Related Media will also be deleted in this case.
     * Finally, error message is displayed in snackBar through error handling process.
     */

    /**
     * createNewMedia(): Method that create new Media based on component forms data and return the
     * list of Ids of created Media
     *
     * @return {BigInt[]} as new Diagnosis
     *
     * If process fails for at least one Media creation, error message is displayed in snackBar
     * through error handling process. Id of Media for which creation did not fail will be return
     * anyway.
     */
   const createNewMedia=   async () => {
      const mediaIdList = []
      // await all Promises be resolved before returning result
      await Promise.all(
        // upc for "util-picture-component": task on each img file of the map
        this.$refs.upc.imgFileObject.map(async (img) => {
          try {
            const formData = new FormData()
            formData.append('storage', img) // fill-in FormData with img file
            // TODO get true date and other form fields below
            formData.append('date', '2022-01-01')
            formData.append('author', 'Bob')
            formData.append('source', 'LPO')
            formData.append('remark', 'Nothing to report')
            // create Media
            const newImg = await this.$axios.$post('media/', formData, {
              headers: {
                accept: 'application/json',
                'Content-Type': 'multipart/form-data',
              },
            })
            mediaIdList.push(newImg.id) // set Media id to mediaIdList
          } catch (_err) {
        console.debug(_err)
        const error: ErrorInfo = {
          code : errorCodes.create_point.code,
          msg : t(`error.${errorCodes.create_point.msg}`)
        }
        errorStore.setError(error)
        back()
          }
        })
      )
      return mediaIdList
    }

</script>
