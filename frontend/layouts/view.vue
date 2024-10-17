<template>
  <v-container class="fill-height pa-0" fluid>
    <v-row class="fill-height">
      <v-col :cols="mobile ? 12 : 6" class="pr-0 pt-0 pb-0"
        :class="mobile ? (isSearchPage ? 'fill-height': 'h-50') : ''">
        <slot name="map">
          <map-search :edit-mode="false" />
        </slot>
      </v-col>
      <v-col :cols="mobile ? 12 : 6" class="pa-0" :class="mobile ? (isSearchPage ? 'fill-height': 'h-50') : ''">
        <slot />
      </v-col>
    </v-row>
    <!--
    <template v-else>
      <v-card class="fill-height" width="100%">
        <v-card-text class="fill-height pa-0">
          <slot name="map">
            <map-search :edit-mode="false" />
          </slot>
        </v-card-text>
      </v-card>
    </template> -->

    <!-- <template v-else>
      <v-row class="fill-height">
        <v-card class="w-100 h-100">
          <v-tabs v-model="tab" bg-color="indigo-darken-2" fixed-tabs>
            <v-tab value="map">Map {{ tab }}</v-tab>
            <v-tab value="content">Content {{ tab }}</v-tab>
          </v-tabs>

          <v-tabs-window v-model="tab" class="fill-height">
            <v-tabs-window-item value="map" class="fill-height pa-0">
              <v-container class="fill-height pa-0" fluid>
                <slot name="map">
                  <map-search :edit-mode="false" />
                </slot>
              </v-container>
            </v-tabs-window-item>
            <v-tabs-window-item value="content">
              <v-container class="fill-height pa-0" fluid>
                <slot />
              </v-container>
            </v-tabs-window-item>
          </v-tabs-window>
        </v-card>
      </v-row>
    </template> -->
  </v-container>
</template>

<script setup lang="ts">
import {computed} from 'vue';
import { useDisplay } from 'vuetify'
const tab=ref('map')
const {mobile} = useDisplay()
const route = useRoute()

const isSearchPage :boolean = computed(() => route.path == '/search')

watch(route, (val) => {
  console.log('route', val)
})

onMounted (() => {
    // TODO fix reactive value
    // mdAndUp.value=true
    console.log('route', route)
})
</script>
