<template>
  <v-card class="my-2" :title="$t('display.diagnosis')" :subtitle="`Réalisé le ${diagnosis.date}`">
    <template #text>
      <span class="font-weight-bold">Recommandations&nbsp;: </span><br>
      <v-chip :prepend-icon="diagnosis.isolation_advice ? 'mdi-exclamation': false"
        :color="[diagnosis.isolation_advice ? 'warning' : '']" class="ma-2">
        {{ diagnosis.isolation_advice ? '' : 'ne pas ' }}{{ $t('diagnosis.isolate') }}
      </v-chip>
      <v-chip :prepend-icon="diagnosis.dissuasion_advice ? 'mdi-exclamation': false"
        :color="[diagnosis.dissuasion_advice ? 'warning' : '']" class="ma-2">
        {{ diagnosis.dissuasion_advice ? '' : 'ne pas ' }}{{ $t('diagnosis.make-dissuasive') }}
      </v-chip>
      <v-chip :prepend-icon="diagnosis.attraction_advice ? 'mdi-exclamation': false"
        :color="[diagnosis.attraction_advice ? 'warning' : '']" class="ma-2">
        {{ diagnosis.attraction_advice ? '' : 'ne pas ' }}{{ $t('diagnosis.make-attractive') }}
      </v-chip>
      <v-chip :prepend-icon="diagnosis.change_advice ? 'mdi-exclamation': false"
        :color="[diagnosis.change_advice == true ? 'warning' : '']" class="ma-2">
        {{ diagnosis.change_advice ? '' : 'ne pas ' }}{{ $t('diagnosis.change-advice') }}
      </v-chip>
      <template v-if="isPoint">
        <p>
          <span class="font-weight-bold">{{ $t('support.support-type') }}&nbsp;:</span><br>
          <v-chip v-for="pt in diagnosis.pole_type" v-if="diagnosis.pole_type.length>0" :key="pt.id" color="info"
            class="ma-2">
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
          <v-icon icon="mdi-circle" :color="riskColors[diagnosis.pole_dangerousness.code]" class="mx-2" /> <span>{{
            diagnosis.pole_dangerousness.label }}</span>
        </p>
      </template>
      <template v-if="isLine">
        <p>
          <span class="font-weight-bold">Intégration bati&nbsp;:</span>
          <v-icon icon="mdi-circle"
            :color="diagnosis?.sgmt_build_integr_risk ? riskColors[diagnosis?.sgmt_build_integr_risk?.code]:'grey'"
            class="mx-2" />
          <span>{{ diagnosis?.sgmt_build_integr_risk?.label}}</span>
        </p>
        <p>
          <span class="font-weight-bold">Déplacement&nbsp;:</span>
          <v-icon icon="mdi-circle" :color="riskColors[diagnosis.sgmt_moving_risk?.code]" class="mx-2" /> <span>{{
            diagnosis.sgmt_moving_risk?.label }}</span>
        </p>
        <p>
          <span class="font-weight-bold">Risque topographique&nbsp;:</span>
          <v-icon icon="mdi-circle" :color="riskColors[diagnosis.sgmt_topo_integr_risk?.code]" class="mx-2" /> <span>{{
            diagnosis.sgmt_topo_integr_risk?.label }}</span>
        </p>
        <p>
          <span class="font-weight-bold">Végétation&nbsp;:</span>
          <v-icon icon="mdi-circle" :color="riskColors[diagnosis.sgmt_veget_integr_risk?.code]" class="mx-2" /> <span>{{
            diagnosis.sgmt_veget_integr_risk?.label }}</span>
        </p>
      </template>
      <p v-if="diagnosis.technical_proposal">
        <span class="font-weight-bold">{{ $t('app.technical_proposal') }}</span>
      </p>
      <p>
        {{ diagnosis.technical_proposal }}
      </p>
      <p v-if="diagnosis.remark">
        <span class="font-weight-bold">{{ $t('app.remark') }}</span>
      </p>
      <p>
        {{ diagnosis.remark }}
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
    <v-card-actions>
      <v-spacer />
      <v-dialog max-width="500">
        <template #activator="{ props: activatorProps }">
          <v-btn v-bind="activatorProps" color="red" text="Supprimer" prepend-icon="mdi-delete-circle" />
        </template>

        <template #default="{ isActive }">
          <v-card title="Suppression d'un diagnostic" color="red" prepend-icon="mdi-alert">
            <v-card-text>
              <div class="my-4">
                Vous êtes sur le point de supprimer un diagnostic, en êtes vous bien certain&nbsp;?
              </div>
              <v-btn color="white" block text="Oui, Supprimer" prepend-icon="mdi-delete-circle" @click="deleteDiag()" />
            </v-card-text>

            <v-card-actions>
              <v-spacer />
              <v-btn text="Annuler" prepend-icon="mdi-close-circle" @click="isActive.value = false" />
            </v-card-actions>
          </v-card>
        </template>
      </v-dialog>
      <v-btn color="orange" prepend-icon="mdi-pencil-circle" @click="updateDiag">Modifier</v-btn>
    </v-card-actions>
    <!-- <pre><code>{{ diagnosis }}</code></pre> -->
  </v-card>


</template>

<script setup lang="ts">

interface Props {
  infrastructureType: string,
  diagnosis: Object,
}

const {infrastructureType, diagnosis} = defineProps<Props>()
const router = useRouter()
const deletedDiagConfirm = ref(true)

const riskColors = reactive({
  RISK_L: 'light-green',
  RISK_M: 'yellow',
  RISK_H: 'red lighten-1 white--text'
})

const stateColors = reactive({
  GOOD: 'light-green',
  POOR: 'yellow',
})

const isPoint= computed(() => infrastructureType==='Point')
const isLine = computed(() => infrastructureType==='Line')

const updateDiag = () => {
  router.push({
    path: `/infrastructures/${diagnosis.infrastructure}/diagnosis`,
    query: {id_diagnosis: diagnosis.id, type:infrastructureType.toLowerCase() }
  })
}

const deleteDiag = async () => {
  await useHttp(`/api/v1/cables/diagnosis/${diagnosis.id}/`, {method: 'delete'})
}

onMounted(()=>{
  console.log('diagnosis',diagnosis)
})

</script>
