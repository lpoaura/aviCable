<template>
  <v-card elevation="0" class="fill-height">
    <v-form ref="form" v-model="formValid" class="text-center">
      <v-toolbar color="pink" dark elevation="0">
        <!-- TODO Review title handling and add terms in locales -->
        <v-toolbar-title>
          {{ newDiag ? 'Nouveau' : 'Modifier le' }}
          {{ diagnosis ? 'Diagnostic' : $t('support.support') }}
        </v-toolbar-title>
        <v-spacer></v-spacer>
        <v-btn icon @click="$router.back()">
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-toolbar>
      <v-card-text class="overflow-auto">
        <v-container v-if="!diagnosis">
          <v-row>
            <v-col cols="12" class="text-left">
              <strong> {{ $t('forms.general-infrastructure') }}</strong>
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="12" md="4">
              <v-text-field
                ref="lat"
                v-model="lat"
                :label="$t('support.latitude')"
                type="number"
                placeholder="Latitude"
                :rules="[rules.requiredOrNotValid, rules.latRange]"
                required
                hide-spin-buttons
                outlined
                dense
              />
            </v-col>

            <v-col cols="12" md="4">
              <v-text-field
                ref="lng"
                v-model="lng"
                :label="$t('support.longitude')"
                type="number"
                :rules="[rules.requiredOrNotValid, rules.lngRange]"
                required
                hide-spin-buttons
                outlined
                dense
              />
            </v-col>
            <v-col cols="12" md="4" v-if="!diagnosis">
              <v-select
                v-model="pointData.owner_id"
                :items="networkOwners"
                item-text="label"
                item-value="id"
                :rules="[rules.required]"
                :label="$t('support.network')"
                outlined
                dense
                required
              >
              </v-select>
            </v-col>
          </v-row>
        </v-container>
        <v-divider></v-divider>
        <v-container>
          <v-row>
            <v-col cols="12" class="text-left">
              <strong>{{ $t('display.diagnosis') }}</strong>
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="12" md="4" v-if="!support">
              <v-menu
                :close-on-content-click="false"
                transition="scale-transition"
              >
                <template #activator="{ on, attrs }">
                  <v-text-field
                    v-model="diagData.date"
                    :label="$t('forms.datecreate')"
                    persistent-hint
                    prepend-icon="mdi-calendar"
                    readonly
                    outlined
                    dense
                    v-bind="attrs"
                    v-on="on"
                  ></v-text-field>
                </template>
                <v-date-picker v-model="diagData.date" no-title></v-date-picker>
              </v-menu> </v-col
            ><v-col cols="12" md="4" v-if="!support">
              <v-select
                v-model="diagData.condition_id"
                :items="conditions"
                item-text="label"
                item-value="id"
                :rules="[rules.required]"
                :label="$t('support.condition')"
                outlined
                dense
              ></v-select>
            </v-col>

            <v-col cols="12" md="4" v-if="!support">
              <v-checkbox
                v-model="diagData.neutralized"
                :label="$t('support.neutralized')"
                dense
              ></v-checkbox>
            </v-col>

            <v-col cols="12" v-if="!support">
              <v-autocomplete
                v-model="diagData.pole_type_id"
                :items="poleTypes"
                item-text="label"
                item-value="id"
                :rules="[rules.required]"
                hide-selected
                :label="$t('support.support-type')"
                multiple
                deletable-chips
                small-chips
                outlined
                dense
              ></v-autocomplete>
            </v-col>
            <v-col cols="12" md="6">
              <v-select
                v-model="diagData.pole_attractivity_id"
                :items="riskLevels"
                item-text="label"
                item-value="id"
                :rules="[rules.required]"
                :label="$t('support.attractiveness')"
                outlined
                dense
              ></v-select>
            </v-col>
            <v-col cols="12" md="6">
              <v-select
                v-model="diagData.pole_dangerousness_id"
                :items="riskLevels"
                item-text="label"
                item-value="id"
                :rules="[rules.required]"
                :label="$t('support.dangerousness')"
                outlined
                dense
              ></v-select>
            </v-col>
            <v-col cols="12" md="4">
              <v-checkbox
                v-model="diagData.isolation_advice"
                :label="$t('support.advice_isol')"
                dense
              ></v-checkbox>
            </v-col>
            <v-col cols="12" md="4">
              <v-checkbox
                v-model="diagData.dissuasion_advice"
                :label="$t('support.advice_disrupt')"
                dense
              ></v-checkbox>
            </v-col>
            <v-col cols="12" md="4">
              <v-checkbox
                v-model="diagData.attraction_advice"
                :label="$t('support.advice_attract')"
                dense
              ></v-checkbox>
            </v-col>

            <v-col cols="12">
              <v-textarea
                v-model="diagData.remark"
                clearable
                clear-icon="mdi-close-circle"
                :label="$t('app.remark')"
                :rules="[rules.textLength]"
                rows="2"
                counter="300"
                outlined
                dense
              ></v-textarea>
            </v-col>
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
              <v-list v-if="diagnosis && !newDiag">
                <v-list-item v-for="img in diagnosis.media" :key="img.id">
                  <v-row>
                    <v-col>
                      <v-img
                        :src="img.storage"
                        max-height="100"
                        max-width="166"
                        class="ma-2"
                      />
                    </v-col>
                    <!-- <v-col>date: {{ pictDate }}</v-col> -->
                    <v-col></v-col>
                    <v-col cols="1">
                      <v-icon small color="red">mdi-trash-can</v-icon>
                    </v-col>
                  </v-row>
                </v-list-item>
              </v-list></v-container
            >
          </v-row>
        </v-container>
      </v-card-text>
      <v-card-actions>
        <v-row class="justify-space-around mb-2">
          <v-btn @click="back">{{ $t('app.cancel') }}</v-btn>
          <v-btn @click="submit">{{ $t('app.valid') }}</v-btn>
        </v-row>
      </v-card-actions>
    </v-form>
  </v-card>
</template>
<script>
import { mapGetters } from 'vuex'
import * as errorCodes from '~/static/errorConfig.json'

export default Vue.extend({
  name: 'PointComponent',

  props: {
    support: { type: Object, default: null },
    diagnosis: { type: Object, default: null },
    operation: { type: Object, default: null },
    newDiag: { type: Boolean, default: null },
  },

  data() {
    return {
      formValid: true,
      // manualChange: false, // boolean to activate manual coordinate change
      // form values
      newLat: null,
      newLng: null,
      // To manage Media
      newCreatedMediaIdList: [],
      // define data related to Point
      pointData: {
        geom: {
          type: 'Point',
          coordinates: this.support ? this.support.coordinates : [],
        },
        owner_id: this.support ? this.support.owner_id : null,
      },
      // define data related to Diagnosis
      diagData: {
        date:
          this.diagnosis && this.newDiag
            ? this.diagnosis.date
            : new Date(Date.now() - new Date().getTimezoneOffset() * 60000)
                .toISOString()
                .substr(0, 10),
        remark: this.diagnosis ? this.diagnosis.remark : null,
        pole_type_id: this.diagnosis
          ? this.diagnosis.pole_type.map((pt) => pt.id)
          : [],
        neutralized: this.diagnosis ? this.diagnosis.neutralized : false,
        condition_id: this.diagnosis ? this.diagnosis.condition.id : null,
        attraction_advice: this.diagnosis
          ? this.diagnosis.attraction_advice
          : false,
        dissuasion_advice: this.diagnosis
          ? this.diagnosis.dissuasion_advice
          : false,
        isolation_advice: this.diagnosis
          ? this.diagnosis.isolation_advice
          : false,
        pole_attractivity_id: this.diagnosis
          ? this.diagnosis.pole_attractivity.id
          : null,
        pole_dangerousness_id: this.diagnosis
          ? this.diagnosis.pole_dangerousness.id
          : null,
        media_id: this.diagnosis ? this.diagnosis.media.map((m) => m.id) : [],
      },
      // rules for form validation
      rules: {
        required: (v) => !!v || this.$t('valid.required'),
        requiredOrNotValid: (v) =>
          v === 0 || !!v || this.$t('valid.required_or_not_valid'),
        latRange: (v) =>
          (v >= 40 && v <= 52) || `${this.$t('valid.range')}40 : 52`,
        lngRange: (v) =>
          (v >= -20 && v <= 20) || `${this.$t('valid.range')}-20 : 20`,
        textLength: (v) =>
          (v || '').length <= 300 || `${this.$t('valid.length')}: 300`,
      },
    }
  },
  computed: {
    /**
     * Getter and Setter for "lat" value.
     * This latitude value is bind v-text-field "lat", and linked with latitude of the LMarker
     * from map-component.
     * When value is commited, it is detected by map-component.vue
     */
    lat: {
      get() {
        return this.newPoint ? this.newPoint.lat : null // avoid bug if newPoint undefined
      },
      // on change in v-text-field, value is set to store.
      set(newVal) {
        this.$store.commit('coordinatesStore/addPointCoord', {
          lat: newVal !== '' ? Number(newVal) : null, // prevent Number('') returns 0
          lng: this.lng,
        })
      },
    },
    /**
     * Getter and Setter for "lng" value.
     * This longitude value is bind v-text-field "lng", and linked with longitude of the LMarker
     * from map-component.
     * When value is commited, it is detected by map-component.vue
     */
    lng: {
      get() {
        return this.newPoint ? this.newPoint.lng : null // avoid bug if newPoint undefined
      },
      // on change in v-text-field, value is set to store.
      set(newVal) {
        this.$store.commit('coordinatesStore/addPointCoord', {
          lat: this.lat,
          lng: newVal !== '' ? Number(newVal) : null, // prevent Number('') returns 0
        })
      },
    },
    // Get values from store
    ...mapGetters({
      newPoint: 'coordinatesStore/newPointCoord',
      conditions: 'nomenclaturesStore/getConditions',
      networkOwners: 'nomenclaturesStore/getOwners',
      poleTypes: 'nomenclaturesStore/getPoleTypes',
      riskLevels: 'nomenclaturesStore/getRiskLevels',
    }),
  },
  methods: {
    /**
     * back(): Method to get back if cancel Point creation.
     *
     * "newPointCoord" reinitialized with lat and lng set to null
     */
    back() {
      this.$store.commit('coordinatesStore/addPointCoord', {
        lat: null,
        lng: null,
      })
      this.$router.back()
    },

    /**
     * submit(): Method to submit the form for Point/Diagnosis/Media creation or update
     * .
     *
     * If process fail at any step, all elements created before are deleted through error handling
     * process.
     */
    async submit() {
      if (this.$refs.form.validate()) {
        // Case of creation of new Point and associated Diagnosis
        if (!this.support && !this.diagnosis) {
          const pointCreated = await this.createNewPoint()
          // new Point (Support) is successfully created
          if (pointCreated) {
            // Create Diagnosis
            await this.createNewDiagnosis(pointCreated.properties.id)
          }
          this.$router.push('/view')
        } else if (this.diagnosis && !this.newDiag) {
          // Case of update of Diagnosis
          await this.updateDiagnosis()
          this.$router.push(`/supports/${this.diagnosis.infrastructure}`)
        } else if (this.diagnosis && this.newDiag) {
          // Case of creation of new Diagnosis on existing Support
          await this.addNewDiagnosis()
          this.$router.push(`/supports/${this.diagnosis.infrastructure}`)
        } else if (this.support) {
          // update of existing Point
          const error = {
            code: 0,
            msg: 'Update of Support not implemented yet',
          }
          // set error message to errorStore and triggers message display through "err"
          // watcher in error-snackbar component
          this.$store.commit('errorStore/setError', error)
        }
      }
    },

    /**
     * createNewPoint(): Method that create new Point based on forms data (cf. this.pointData)
     *
     * @return {JSON object} as new Point
     *
     * If process fails, error message is displayed in snackBar through error handling process.
     */
    async createNewPoint() {
      try {
        this.pointData.geom.coordinates = [this.lng, this.lat]
        return await this.$axios.$post('cables/points/', this.pointData)
      } catch (_err) {
        const error = {}
        error.code = errorCodes.create_point.code
        error.msg = $nuxt.$t(`error.${errorCodes.create_point.msg}`)
        // set error message to errorStore and triggers message display through "err" watcher in
        // error-snackbar component
        this.$store.commit('errorStore/setError', error)
        this.back()
      }
    },

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
    async createNewDiagnosis(infrstr_id) {
      // Create Media as selected in component form and get list of Ids of created Media
      const mediaIdList = await this.createNewMedia()
      try {
        this.diagData.infrastructure = infrstr_id // set Infrastructure (Point) id
        this.diagData.media_id = mediaIdList // set Media id list
        // Create Diagnosis
        return await this.$axios.$post('cables/diagnosis/', this.diagData)
      } catch (_err) {
        // If Diagnosis creation fails, related infrastructure(Point) is deleted
        await this.$axios.$delete(`cables/points/${infrstr_id}/`)
        // If Diagnosis creation fails, related Media created are deleted
        if (this.newCreatedMediaIdList) {
          this.newCreatedMediaIdList.forEach(
            async (media_id) => await this.$axios.$delete(`/media/${media_id}/`)
          )
        }
        // Error display
        const error = {}
        error.code = errorCodes.create_pole_diagnosis.code
        error.msg = $nuxt.$t(`error.${errorCodes.create_pole_diagnosis.msg}`)
        // set error message to errorStore and triggers message display through "err" watcher / in error-snackbar component
        this.$store.commit('errorStore/setError', error)
        this.back()
      }
    },

    /**
     * addNewDiagnosis(): Method that create new Diagnosis based on forms data (cf.this.diagData)
     * on an existing Support
     *
     * Error handling: A Diagnosis should be created at time of Infrastructure (Point) creation.
     * If Diagnosis creation fails, related Infrastructure (Point) will be deleted.
     * Related Media will also be deleted in this case.
     * Finally, error message is displayed in snackBar through error handling process.
     */
    async addNewDiagnosis() {
      // Create Media as selected in component form and get list of Ids of created Media
      const mediaIdList = await this.createNewMedia()
      try {
        this.diagData.infrastructure = this.diagnosis.infrastructure // set Infrastructure (Point) id
        this.diagData.media_id = mediaIdList // set Media id list
        // Create Diagnosis
        return await this.$axios.$post('cables/diagnosis/', this.diagData)
      } catch (_err) {
        // If Diagnosis creation fails, related Media created are deleted
        if (this.newCreatedMediaIdList) {
          this.newCreatedMediaIdList.forEach(
            async (media_id) => await this.$axios.$delete(`/media/${media_id}/`)
          )
        }
        // Error display
        const error = {}
        error.code = errorCodes.create_pole_diagnosis.code
        error.msg = $nuxt.$t(`error.${errorCodes.create_pole_diagnosis.msg}`)
        // set error message to errorStore and triggers message display through "err" watcher / in error-snackbar component
        this.$store.commit('errorStore/setError', error)
        this.back()
      }
    },

    /**
     * updateDiagnosis(): Method that update Diagnosis based on forms data (cf.this.diagData)
     *
     * Error handling: If Diagnosis update fails, new created Media will be deleted.
     * Finally, error message is displayed in snackBar through error handling process.
     */
    async updateDiagnosis() {
      // Create new Media as selected in component form and get list of Ids of created Media
      const mediaIdList = await this.createNewMedia()
      try {
        this.diagData.infrastructure = this.diagnosis.infrastructure // set Infrastructure (Point) id
        this.diagData.media_id = mediaIdList // set Media id list
        // Create Diagnosis
        return await this.$axios.$put(
          `cables/diagnosis/${this.diagnosis.id}/`,
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
    },

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
    async createNewMedia() {
      const mediaIdList = !this.newDiag ? this.diagData.media_id : []

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
            this.newCreatedMediaIdList.push(newImg.id)
          } catch (_err) {
            const error = {}
            error.code = errorCodes.img_sending.code
            error.msg = $nuxt.$t(`error.${errorCodes.img_sending.msg}`)
            // set error message to errorStore and triggers message display through "err"
            // watcher in error-snackbar component
            this.$store.commit('errorStore/setError', error)
          }
        })
      )
      return mediaIdList
    },
  },
})
</script>
