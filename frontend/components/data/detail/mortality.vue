<template>
  <v-layout v-if="data.id" full-height>
    <v-app-bar density="compact" color="blue-grey-lighten-5">
      <v-app-bar-title>
        <v-chip :prepend-icon="deathCauseIcons[data.properties?.death_cause.code] || 'mdi-help'" color="red">{{ data.id
          }}</v-chip>&nbsp;{{ $t('display.mortalityCases')}}<strong>&nbsp;: {{ data.properties.species.vernacular_name
          }}</strong>
      </v-app-bar-title>
      <v-spacer />
      <v-app-bar-nav-icon>
        <v-btn density="compact" icon="mdi-close" @click="$router.push('/search')" />
      </v-app-bar-nav-icon>
    </v-app-bar>
    <v-main scrollable>
      <v-container>
        <data-card-mortality :item="data" :item-id="data.id" />
      </v-container>
    </v-main>
  </v-layout>
</template>

<script setup lang="ts">
// const router = useRouter()
const {data} = defineProps(['data'])
const deathCauseIcons = ref({
  COD_EL: 'mdi-lightning-bolt',
  COD_IM:'mdi-star',
  COD_UNKNOWN: 'mdi-help'
})
console.debug('props.data' , data)
</script>
