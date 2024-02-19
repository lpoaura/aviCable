<template>
  <v-card class="my-2">
    <v-layout>
      <v-app-bar density="compact" color="blue-grey-lighten-4">
        <v-app-bar-title>
          {{ $t('display.diagnosis') }}
        </v-app-bar-title>
        <v-spacer />
        <v-btn-toggle rounded="0" density="compact">
          <v-btn class="mr-2" v-if="diagnosis.last" color="green" density="compact" icon="mdi-eye-plus-outline"
            @click="newDiag" />
          <v-btn class="mr-2" variant="elevated" density="compact" icon="mdi-pencil" color=orange @click="updateDiag" />
        </v-btn-toggle>
      </v-app-bar>
      <v-main>
        <v-card-subtitle class="ma-2">
          Diagnostic réalisé le {{ diagnosis.date }}
        </v-card-subtitle>
        <v-card-text>
          <span class="font-weight-bold">Recommandations</span>
          <v-layout class="d-flex justify-space-between">
            <v-chip :color="[diagnosis.isolation_advice ? 'warning' : '']" class="ma-2">
              {{ diagnosis.isolation_advice ? '' : 'ne pas ' }}{{ $t('diagnosis.isolate') }}
            </v-chip>
            <v-chip :color="[diagnosis.dissuasion_advice ? 'warning' : '']" class="ma-2">
              {{ diagnosis.dissuasion_advice ? '' : 'ne pas ' }}{{ $t('diagnosis.make-dissuasive') }}
            </v-chip>
            <v-chip :class="[diagnosis.attraction_advice ? 'warning' : '']" class="ma-2">
              {{ diagnosis.attraction_advice ? '' : 'ne pas ' }}{{ $t('diagnosis.make-attractive') }}
            </v-chip>
          </v-layout>
          <p>
            <span class="font-weight-bold">{{ $t('support.condition') }}</span>
            <v-chip :color="diagnosis.condition ? stateColors[diagnosis.condition.code] :'grey'" variant="elevated"
              class="ma-2">
              {{ diagnosis.condition?.label }}
            </v-chip>
          </p>
          <p>
            <span class="font-weight-bold">{{ $t('support.support-type') }}</span>
            <v-chip v-if="diagnosis.pole_type.length>0" v-for="pt in diagnosis.pole_type" :key="pt.id" class="ma-2">
              {{ pt.label }}
            </v-chip>
            <span v-else>&nbsp;- </span>
          </p>
          <p>
            <span class="font-weight-bold">{{ $t('support.attractiveness') }}</span>
            <v-chip :color="diagnosis?.pole_attractivity ? riskColors[diagnosis?.pole_attractivity.code]:'grey'"
              variant="elevated" class="ma-2">
              {{ diagnosis?.pole_attractivity.label}}
            </v-chip>
          </p>
          <p>
            <span class="font-weight-bold">{{ $t('support.dangerousness') }}</span>
            <v-chip :color="riskColors[diagnosis.pole_dangerousness.code]" variant="elevated" class="ma-2">
              {{ diagnosis.pole_dangerousness.label }}
            </v-chip>
          </p>
          <p v-if="diagnosis.technical_proposal">
            <span class="font-weight-bold">{{ $t('app.technical_proposal') }}</span>
            <p>
              {{ diagnosis.technical_proposal }}
            </p>
          </p>
          <p v-if="diagnosis.remark">
            <span class="font-weight-bold">{{ $t('app.remark') }}</span>
            <p>
              {{ diagnosis.remark }}
            </p>
          </p>
          <v-list>
            <v-list-item v-for="img in diagnosis.media" :key="img.id">
              <v-row>
                <v-col>
                  <v-img :src="img.storage" max-height="100" max-width="166" class="ma-2" />
                </v-col>
                <!-- <v-col>date: {{ pictDate }}</v-col>   -->
                <v-col />
                <v-col cols="1">
                  <v-icon size="small" color="red">
                    mdi-trash-can
                  </v-icon>
                </v-col>
              </v-row>
            </v-list-item>
          </v-list>
        </v-card-text>
      </v-main>
    </v-layout>
    <!-- <pre><code>{{ diagnosis }}</code></pre> -->
  </v-card>
</template>

<script setup>

const {diagnosis} = defineProps(['diagnosis'])
const router = useRouter()

const riskColors = reactive({
  RISK_L: 'light-green',
  RISK_M: 'yellow',
  RISK_H: 'red lighten-1 white--text'
})

const stateColors = reactive({
  GOOD: 'light-green',
  POOR: 'yellow',
})

const newDiag = () => {
  console.debug(`/supports/${diagnosis.infrastructure}/diagnosis`)
  router.push({
    path: `/supports/${diagnosis.infrastructure}/diagnosis`,
    query: { modifyDiag: 'false' }
  })
}
const updateDiag = () => {
  router.push({
    path: `/supports/${diagnosis.infrastructure}/diagnosis`,
    query: { modifyDiag: 'true', id_diagnosis: diagnosis.id }
  })
}

onMounted(()=>{
  console.log('diagnosis',diagnosis)
})

</script>
