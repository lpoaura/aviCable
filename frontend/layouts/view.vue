<template>
  <v-container class="fill-height pa-0" fluid>
    <v-row v-if="!mobile" class="fill-height">
      <v-col cols="6" class="pr-0 pt-0 pb-0">
        <slot name="map">
          <map-search :edit-mode="false" />
        </slot>
      </v-col>
      <v-col cols="6" class="pa-0 fill-height">
        <slot />
      </v-col>
    </v-row>

    <template v-if="mobile">
      <v-card class="fill-height" width="100%">
        <v-card-text class="fill-height pa-0">
          <slot name="map">
            <map-search :edit-mode="false" />
          </slot>
        </v-card-text>
      </v-card>
    </template>
  </v-container>
</template>

<script setup lang="ts">
import { useDisplay } from 'vuetify'
const tab=ref('map')
const {mobile} = useDisplay()

onMounted (() => {
    // TODO fix reactive value
    // mdAndUp.value=true
})
</script>
