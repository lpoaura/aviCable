<template>
  <v-container class="fill-height pa-0" fluid>
    <v-row class="fill-height">
      <v-col :cols="mobile ? 12 : 6" class="pr-0 pt-0 pb-0"
        :class="mobile ? (isSearchPage ? 'fill-height' : 'h-50') : ''">
        <slot name="map">
          <map-search :edit-mode="false" />
        </slot>
      </v-col>
      <v-col  v-if="!(mobile && isSearchPage)" :cols="mobile ? 12 : 6" class="pa-0" :class="mobile ? (isSearchPage ? 'fill-height' : 'h-50') : ''">
        <slot />
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useDisplay } from 'vuetify'
const { mobile } = useDisplay()
const route = useRoute()

const isSearchPage: Computed<boolean> = computed(() => route.path == '/search')


</script>
