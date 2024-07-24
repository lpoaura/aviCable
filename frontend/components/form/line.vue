<template>
  <v-card elevation="0" class="fill-height">
    <v-layout>
      <v-form ref="form" v-model="formValid" class="text-center">
        <v-app-bar color="pink" flat dark density="compact">
          <template v-slot:prepend>
            <v-btn icon="mdi-pencil-circle"></v-btn>
            <v-app-bar-title>{{ modifyDiag ? 'Modifier le' : 'Nouveau' }}
              {{ $t('line.new_segment') }}
            </v-app-bar-title>
          </template>
          <template v-slot:append>
            <v-btn icon="mdi-close" @click="router.back()" />
          </template>
        </v-app-bar>
        <v-main>
          <v-card-text class="fill-height overflow-auto">
            <v-container>
              <v-row>
                <v-col cols="12" class="text-left">
                  <strong>{{ $t('forms.general') }}</strong>
                </v-col>
              </v-row>
              <v-row>
                <v-col cols="12" lg="6">
                  <v-select v-model="lineData.owner_id" :items="networkOwners" item-title="label" item-value="id"
                    :rules="[rules.required]" :label="$t('support.network')" variant="solo" density="compact" required>
                  </v-select>
                </v-col>

                <v-col cols="12" lg="6">
                  <v-menu :close-on-content-click="false" transition="scale-transition">
                    <template v-slot:activator="{ props }">
                      <v-text-field v-model="diagData.date" :label="$t('forms.datecreate')" persistent-hint
                        prepend-icon="mdi-calendar" readonly variant="solo" density="compact"
                        v-bind="props"></v-text-field>
                    </template>
                    <v-date-picker v-model="diagData.date" no-title></v-date-picker>
                  </v-menu>
                </v-col>

                <v-col cols="12">
                  <v-checkbox v-model="diagData.neutralized" :label="$t('support.neutralized')"
                    density="compact"></v-checkbox>
                </v-col>
                <v-col cols="12">
                  <v-textarea v-model="diagData.remark" clearable clear-icon="mdi-close-circle" :label="$t('app.remark')"
                    :rules="[rules.textLength]" rows="2" counter="300" variant="solo" density="compact"></v-textarea>
                </v-col>
              </v-row>
            </v-container>
            <!-- Filedset GENERAL INFORMATION -->
            <v-container>
              <v-row>
                <v-col cols="12" class="text-left">
                  <strong>{{ $t('forms.risk_assessment') }}</strong>
                </v-col>
              </v-row>
              <v-row>
                <v-col cols="12" lg="6">
                  <v-select v-model="diagData.buildIntegRisk" :items="riskLevels" item-title="label" item-value="id"
                    :rules="[rules.required]" :label="$t('line.buildIntegRisk')" variant="solo"
                    density="compact"></v-select>
                </v-col>
                <v-col cols="12" lg="6">
                  <v-select v-model="diagData.movingRisk" :items="riskLevels" item-title="label" item-value="id"
                    :rules="[rules.required]" :label="$t('line.movingRisk')" variant="solo" density="compact"></v-select>
                </v-col>

                <v-col cols="12" lg="6">
                  <v-select v-model="diagData.topoIntegRisk" :items="riskLevels" item-title="label" item-value="id"
                    :rules="[rules.required]" :label="$t('line.topoIntegRisk')" variant="solo"
                    density="compact"></v-select>
                </v-col>
                <v-col cols="12" lg="6">
                  <v-select v-model="diagData.vegetIntegRisk" :items="riskLevels" item-title="label" item-value="id"
                    :rules="[rules.required]" :label="$t('line.vegetIntegRisk')" variant="solo"
                    density="compact"></v-select>
                </v-col>
              </v-row>
            </v-container>
          </v-card-text>
          <v-card-actions>
            <v-row class="justify-space-around mb-2">
              <v-btn color="red" variant="elevated" prepend-icon="mdi-close" @click="back">{{ $t('app.cancel')
                }}</v-btn>
              <v-btn color="green" variant="elevated" prepend-icon="mdi-check" @click="submit">{{ $t('app.valid')
                }}</v-btn>
            </v-row>
          </v-card-actions>
        </v-main>
      </v-form>
    </v-layout>
  </v-card>
</template>

<script setup lang="ts">
import * as errorCodes from '~/static/errorConfig.json'

// init modules
const {t} = useI18n()
const router = useRouter()
const route = useRoute()

// init Stores
const coordinatesStore = useCoordinatesStore()
const nomenclaturesStore = useNomenclaturesStore()

const {line, diagnosis, operation} = defineProps(['line', 'diagnosis', 'operation'])

// data

const modifyDiag = computed(() => route.query.modifyDiag === 'true' ? true : false)

const formValid = ref(true)
     const  manualChange= ref(false)
      // define data related to Point
      const lineData = reactive({
        geom: coordinatesStore.newGeoJSONLine,
        owner_id: 1, // null,
      })
      // define data related to Diagnosis
      const diagData = reactive({
        date:diagnosis && !modifyDiag
          ? diagnosis.date
          : new Date(Date.now() - new Date().getTimezoneOffset() * 60000)
              .toISOString().substr(0, 10),
        remark: diagnosis ? diagnosis.remark : null,
        pole_type_id: diagnosis
      ? diagnosis.pole_type.map((pt) => pt.id)
      : [], // null,
        neutralized: diagnosis ? diagnosis.neutralized : false,
        buildIntegRisk: null,
        movingRisk: null,
        topoIntegRisk: null,
        vegetIntegRisk: null,
      })
      // rules for form validation
const rules = reactive({
  required: (v: string | number) => !!v || t('valid.required'),
  requiredOrNotValid: (v: string | number) => v === 0 || !!v || t('valid.required_or_not_valid'),
  latRange: (v: number) => (v >= 40 && v <= 52) || `${t('valid.range')}40 : 52`,
  lngRange: (v: number) => (v >= -20 && v <= 20) || `${t('valid.range')}-20 : 20`,
  textLength: (v: string) => (v || '').length <= 300 || `${t('valid.length')}: 300`,
})

const networkOwners = computed(() => nomenclaturesStore.ownerItems)
const riskLevels = computed(() => nomenclaturesStore.riskLevelItems)

const back = () => {
  coordinatesStore.setNewGeoJSONLine({coordinates: [], type: 'LineString'})
  router.back()
}

const submit = async () => {
      // if (formValid) { {
      //   let lineCreated = null
      //   const mediaIdList = []
      //   let diagCreated = null
      //   // Create new segment (Line infrastructure)
      //   try {
      //     lineData.geom.coordinates = newLineCoord
      //     lineCreated = await useHttp('/api/v1/cables/lines/', {method: 'post', body: lineData})
      //   } catch (err) {
      //     const error = {}
      //     error.code = errorCodes.create_line.code
      //     error.msg = $nuxt.$t(`error.${errorCodes.create_line.msg}`)
      //     // set error message to errorStore and triggers message display through "err" watcher in
      //     // error-snackbar component
      //     this.$store.commit('errorStore/setError', error)
      //     // this.$router.push('/search')
      //     this.back()
      //   }
      //   // new Line is successfully created
      //   if (lineCreated) {
      //     // Create Diagnosis
      //     try {
      //       this.diagData.infrastructure = lineCreated.properties.id
      //       this.diagData.media_id = mediaIdList
      //       diagCreated = await this.$axios.$post(
      //         'cables/diagnosis/',
      //         this.diagData
      //       )
      //       this.$router.push('/search')
      //     } catch (_err) {
      //       // if no new Diagnosis created
      //       if (!diagCreated) {
      //         // if new Line was created before, delete it
      //         if (lineCreated) {
      //           await this.$axios.$delete(
      //             `cables/lines/${lineCreated.properties.id}/`
      //           )
      //         }
      //       }
      //       // Error display
      //       const error = {}
      //       error.code = errorCodes.create_line_diagnosis.code
      //       error.msg = $nuxt.$t(
      //         `error.${errorCodes.create_line_diagnosis.msg}`
      //       )
      //       // set error message to errorStore and triggers message display through "err" watcher / in error-snackbar component
      //       this.$store.commit('errorStore/setError', error)
      //       this.back()
      //     }
      //   }
      // }
      // }
      }
</script>


<style>
/* .v-tab {
  width: 100px;
  background-color: 'indigo';
}

.v-btn {
  width: 80px;
}

/* .v-text-field,
.v-select,
.v-checkbox {
  width: 200px;
} */

/*
.v-textarea {
  min-width: 500px;
}

.v-chip {
  margin: 2px;
} */
</style>
