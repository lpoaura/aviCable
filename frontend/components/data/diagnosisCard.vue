<template>
  <v-card class="my-2" :title="$t('display.diagnosis')" :subtitle="`Réalisé le ${diagnosis.date}`">

    <template v-slot:text>
      <span class="font-weight-bold">Recommandations&nbsp;:</span><br>
      <v-chip :color="[diagnosis.isolation_advice ? 'warning' : '']" class="ma-2">
        {{ diagnosis.isolation_advice ? '' : 'ne pas ' }}{{ $t('diagnosis.isolate') }}
      </v-chip>
      <v-chip :color="[diagnosis.dissuasion_advice ? 'warning' : '']" class="ma-2">
        {{ diagnosis.dissuasion_advice ? '' : 'ne pas ' }}{{ $t('diagnosis.make-dissuasive') }}
      </v-chip>
      <v-chip :class="[diagnosis.attraction_advice ? 'warning' : '']" class="ma-2">
        {{ diagnosis.attraction_advice ? '' : 'ne pas ' }}{{ $t('diagnosis.make-attractive') }}
      </v-chip>
      <p>
        <span class="font-weight-bold">{{ $t('support.condition') }}&nbsp;:</span>
        <v-icon icon="mdi-circle" :color="diagnosis.condition ? stateColors[diagnosis.condition.code] :'grey'"
          class="mx-2" />
        <span>{{ diagnosis.condition?.label }}</span>
      </p>
      <p>
        <span class="font-weight-bold">{{ $t('support.support-type') }}&nbsp;:</span><br>
        <v-chip v-if="diagnosis.pole_type.length>0" v-for="pt in diagnosis.pole_type" :key="pt.id" class="ma-2">
          {{ pt.label }}
        </v-chip>
        <span v-else>&nbsp;- </span>
      </p>
      <p>
        <span class="font-weight-bold">{{ $t('support.attractiveness') }}&nbsp;:</span>
        <v-icon icon="mdi-circle"
          :color="diagnosis?.pole_attractivity ? riskColors[diagnosis?.pole_attractivity.code]:'grey'" class="mx-2" />
        <span>{{ diagnosis?.pole_attractivity.label}}</span>
      </p>
      <p>
        <span class="font-weight-bold">{{ $t('support.dangerousness') }}&nbsp;:</span>
        <v-icon icon="mdi-circle" :color="riskColors[diagnosis.pole_dangerousness.code]" class="mx-2">
        </v-icon> <span>{{ diagnosis.pole_dangerousness.label }}</span>
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
    </template>
    <template v-slot:actions>
      <v-btn v-if="diagnosis.last" color="green" @click="newDiag"><v-icon>mdi-eye-plus</v-icon> Nouveau</v-btn>
      <v-btn color="orange" @click="updateDiag"><v-icon>mdi-pencil</v-icon> Modifier</v-btn>
    </template>
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
