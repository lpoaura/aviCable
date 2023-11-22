<template>
  <v-data-table :headers="headers" :items="SADataFeatures" :items-per-page="5" class="elevation-1" />
</template>

<script>
import { mapState } from 'pinia'
import { useSensitiveAreasStore } from '~/store/sensitiveAreasStore'

export default {
  name: 'SensAreaDisplay',
  data() {
    return {
      headers: [
        {
          text: 'ID Zone Sensible',
          align: 'start',
          sortable: true,
          value: 'id'
        },
        { text: 'Name', value: 'properties.name' },
        { text: 'Code', value: 'properties.code' }
      ]
    }
  },
  /** Fetch Sensitive Area from backend and record it to Nuxt Store */
  async fetch() {
    const data = await useHttp('/api/v1/sensitive-areas/') // get FeatureCollection
    this.$store.commit('saStore/add', data)
  },
  /** Gather Sensitive Area data from Nuxt Store */
  computed: { ...mapState(useSensitiveAreasStore, ['SaDataFeature']) }
}
</script>
