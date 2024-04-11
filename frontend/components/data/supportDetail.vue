<template>
  <v-layout full-height>
    <v-app-bar density="compact" color="blue-grey-lighten-5">
      <v-app-bar-title>
        #{{data.properties.id}} {{ $t('support.support') }}
        <strong>{{ data.properties.owner.label }}</strong>
      </v-app-bar-title>

      <v-spacer />
      <v-chip :prepend-icon="neutralized ? 'mdi-check-circle-outline': 'mdi-alert-outline'" small
        class="mr-2" :color="neutralized ? 'success' : 'error'" variant="elevated">
        {{ neutralized ? 'neutralisé' : 'à neutraliser' }}
      </v-chip>
      <v-app-bar-nav-icon>
        <v-btn density="compact" icon="mdi-close" @click="$router.back()" />
      </v-app-bar-nav-icon>
    </v-app-bar>
    <v-main scrollable>
      <v-container>
        <v-card class="my-2">
          <v-layout>
            <v-app-bar density="compact" color="blue-grey-lighten-4">
              <v-app-bar-title>Info Support </v-app-bar-title><v-spacer />
              <v-btn density="compact" icon="mdi-pencil" color="orange" @click="$router.push('/search')" />
            </v-app-bar>
            <v-main>
              <v-card-text>
                <v-row>
                  <v-col cols="12" lg="6">
                    <p class="text-strong" v-if="data.properties.geo_area.length > 0">
                      Limites administratives
                    </p>

                    <v-chip v-for="(ga, index) in data.properties.geo_area" :key="index">
                      {{ ga.name }} ({{ ga.code }})
                    </v-chip>
                  </v-col>
                  <v-col cols="12" lg="6">
                    <p v-if="data.properties.sensitive_area.length > 0">
                      Zones sensibles
                    </p>
                    <v-chip v-for="sa in data.properties.sensitive_area" :key="sa.id">
                      {{ sa.name }} {{ sa.name }}
                    </v-chip>
                  </v-col>
                  <v-col cols="12" v-if="lastDiag && lastDiag.pole_type.length">
                    <p>Type de support</p>
                    <!-- <pre>{{ lastDiag }}</pre> -->
                    <v-chip v-for="pt in lastDiag?.pole_type" :key="pt.id">
                      <pre>{{ pt.label }}</pre>
                    </v-chip>
                  </v-col>
                </v-row>
              </v-card-text>
            </v-main>
          </v-layout>
        </v-card>
        <data-diagnosis-card :diagnosis="lastDiag" />
        <data-operation-card v-if="lastOp" :operation="lastOp" />
        <!-- <v-card class="my-2" v-if="previousActions.length">
          <v-layout>
            <v-app-bar density="compact" color="blue-lighten-2" @click="expandHistory = !expandHistory">
              <v-app-bar-title> {{ $t('support.history') }} </v-app-bar-title><v-spacer />
              <v-btn density="compact" :icon="expandHistory ? 'mdi-chevron-up':'mdi-chevron-down'" />
            </v-app-bar>
            <v-main :class="expandHistory? 'ma-2':''">
              <div v-show="expandHistory" v-for="action in previousActions" :key="action.id">
                <data-diagnosis-card v-if="action.resourcetype === 'Diagnosis'" :diagnosis="action" />
                <data-operation-card v-if="action.resourcetype === 'Operation'" :operation="action" />
              </div>
            </v-main>
          </v-layout>
        </v-card> -->

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

const neutralized : boolean = computed(() => {
  return data?.properties.operations.length>0
})

const lastOp = computed(() => {
  return data?.properties.operations.find(
        (action: {  last: boolean }) =>
          action.last
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
