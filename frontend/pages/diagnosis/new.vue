<template>
  <v-container fill-height fluid class="pa-0">
    <v-row v-if="$vuetify.breakpoint.lgAndUp" class="fill-height">
      <v-col cols="6" class="pr-0 pt-0 pb-0">
        <map-component :edit-mode="true" mode="point" />
      </v-col>
      <v-col cols="6" class="pa-0" style="background-color: red">
        <form-point-component :diagnosis="data" :new-diag="newDiag" />
      </v-col>
    </v-row>
    <v-tabs
      v-if="$vuetify.breakpoint.mdAndDown"
      fixed-tabs
      background-color="indigo"
      dark
    >
      <v-tab> {{ $t('app.map') }} </v-tab>
      <v-tab-item>
        <map-component :edit-mode="true" mode="point" />
      </v-tab-item>
      <v-tab> {{ $t('app.data') }} </v-tab>
      <v-tab-item>
        <form-point-component :diagnosis="data" :new-diag="newDiag" />
      </v-tab-item>
    </v-tabs>
  </v-container>
</template>

<script>
import Vue from 'vue'

export default Vue.extend({
  name: 'UpdateDiagnosisPage',
  /**
   * asyncData(): Method that gather data before page be created
   *
   * @param {$axios, query} $axios allow to send request to data through $axios, and query
   * allows to access diagnosis id from URL. New diagnosis will be created from default data
   * of this selected diagnosis
   * with "https://PATH/diagnosis/new?OriginDiagId=16" => new diagnosis will be created with
   * initial default data matching to diagnosis id=16
   */
  async asyncData({ $axios, query }) {
    return {
      data: await $axios.$get(`cables/diagnosis/${query.OriginDiagId}`),
    }
  },
  data() {
    return {
      drawer_opened: true, // drawer closed by default
      miniVariant: true, // small drawer when opening by default
      newDiag: true, // boolean set to true to configure Diagnosis form to Diagnosis creation
    }
  },
})
</script>
