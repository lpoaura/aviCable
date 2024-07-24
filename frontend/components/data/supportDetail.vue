<template>
  <v-layout full-height>
    <v-app-bar density="compact" color="blue-grey-lighten-5">
      <v-app-bar-title>
        #{{data.properties.id}} {{ $t('support.support') }}
        <strong>{{ data.properties.owner.label }}</strong>
      </v-app-bar-title>

      <v-spacer />
      <v-chip :prepend-icon="neutralized ? 'mdi-check-circle-outline': 'mdi-alert-outline'" small class="mr-2"
        :color="neutralized ? 'success' : 'error'" variant="elevated">
        {{ neutralized ? 'neutralisé' : 'pas neutralisé' }}
      </v-chip>
      <v-app-bar-nav-icon>
        <v-btn density="compact" icon="mdi-close" @click="$router.back()" />
      </v-app-bar-nav-icon>
    </v-app-bar>
    <v-main scrollable>
      <v-container>
        <data-support-card :data="data"></data-support-card>
        <data-diagnosis-card v-if="lastDiag" :diagnosis="lastDiag" />
        <data-operation-card v-if="lastOp" :operation="lastOp" :supportId="data.properties.id"/>

        <v-card class="my-2" >
          <v-layout>
            <v-app-bar density="compact" color="blue-lighten-2" @click="expandHistory = !expandHistory">
              <v-app-bar-title> {{ $t('support.history') }} </v-app-bar-title><v-spacer />
              <v-chip prepend-icon="mdi-list-status">{{ otherDiags.length }}</v-chip>&nbsp;
              <v-chip prepend-icon="mdi-cog">{{ otherOps.length }}</v-chip>
              <v-btn density="compact" :icon="expandHistory ? 'mdi-chevron-up':'mdi-chevron-down'" />
            </v-app-bar>
            <v-main :class="expandHistory? 'ma-2':''">
              <div v-if="expandHistory" >
                <data-diagnosis-card v-for="diag in otherDiags" :key="diag.id" :diagnosis="diag" />
                <data-operation-card v-for="ops in otherOps" :key="ops.id"  :operation="ops" />
              </div>
            </v-main>
          </v-layout>
        </v-card>

      </v-container>
    </v-main>
  </v-layout>
</template>

<script setup lang="ts">


const {data} = defineProps(['data'])

console.log('props.data' , data)

const expandHistory=ref(false)

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

const neutralized : boolean = computed(() => {
  return data?.properties.operations.length>0
})

const lastOp = computed(() => {
  return data?.properties.operations.find(
        (action: {  last: boolean }) =>
          action.last
      )
})

const otherOps = computed(() => {
  return data?.properties.operations.filter(
        (action: { last: boolean }) =>
           !action.last
      )
})
// const previousActions = computed(() => {
//   return data?.properties.actions_infrastructure.filter(
//         (action: { last: boolean }) => !action.last
//       )
// })

onMounted(() =>{
  console.log('lastDiag', lastDiag)
})

</script>
