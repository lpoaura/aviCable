<template>
  <v-layout full-height>
    <v-app-bar density="compact" color="blue-grey-lighten-5">
      <v-app-bar-title>
        <v-chip prepend-icon="mdi-eye-circle-outline" color="primary">
          {{ data.properties.id }}
        </v-chip>&nbsp;{{ type === 'Point' ? $t('support.support') : $t('line.line') }}
        <strong>{{ data.properties.owner.label }}</strong>
      </v-app-bar-title>

      <v-spacer />

      <v-app-bar-nav-icon>
        <v-btn density="compact" icon="mdi-close" @click="$router.push('/search')" />
      </v-app-bar-nav-icon>
    </v-app-bar>
    <v-main scrollable>
      <v-container>
        <data-card-infrastructure :data="data" />
        <data-card-mortality-for-infrastructure :data="data.properties.mortality" />
        <data-card-diagnosis v-if="lastDiag" :diagnosis="lastDiag" :infrastructure-type="type" />
        <data-card-operation v-if="lastOp" :operation="lastOp" :support-id="data.properties.id"
          @delete="$emit('update')" />
        <v-card class="my-2">
          <v-layout>
            <v-app-bar density="compact" color="blue-lighten-2" @click="expandHistory = !expandHistory">
              <v-app-bar-title> {{ $t('support.history') }} </v-app-bar-title><v-spacer />
              <v-chip prepend-icon="mdi-list-status">{{ otherDiags.length }}</v-chip>&nbsp;
              <v-chip prepend-icon="mdi-cog">{{ otherOps.length }}</v-chip>
              <v-btn density="compact" :icon="expandHistory ? 'mdi-chevron-up' : 'mdi-chevron-down'" />
            </v-app-bar>
            <v-main :class="expandHistory ? 'ma-2' : ''">
              <div v-if="expandHistory">
                <data-card-diagnosis v-for="diag in otherDiags" :key="diag.id" :diagnosis="diag" :type="type" />
                <data-card-operation v-for="ops in otherOps" :key="ops.id" :operation="ops" />
              </div>
            </v-main>
          </v-layout>
        </v-card>

      </v-container>
    </v-main>
  </v-layout>
</template>

<script setup lang="ts">
import type { Feature } from 'geojson'

interface Props {
  // type: string,
  data: Feature
}

const { data } = defineProps<Props>()

const expandHistory = ref(false)

const lastDiag = computed(() => {
  return data?.properties.diagnosis.find(
    (action: { last: boolean }) =>
      action.last
  )
})

const otherDiags = computed(() => {
  return data?.properties.diagnosis.filter(
    (action: { last: boolean }) =>
      !action.last
  )
})

const neutralized: boolean = computed(() => {
  return data?.properties.operations.length > 0
})

const lastOp = computed(() => {
  return data?.properties.operations.find(
    (action: { last: boolean }) =>
      action.last
  )
})

const type = computed(() => {
  return data?.resourcetype
})

const otherOps = computed(() => {
  return data?.properties.operations.filter(
    (action: { last: boolean }) =>
      !action.last
  )
})


</script>
