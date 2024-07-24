<template>
  <v-card class="my-2" :title="$t('display.diagnosis')" :subtitle="`Réalisé le ${diagnosis.date}`">
    <template v-slot:text>
      <span class="font-weight-bold">Recommandations&nbsp;:</span><br>
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
      <p>
        <span class="font-weight-bold">{{ $t('support.condition') }}&nbsp;:</span>
        <v-icon icon="mdi-circle" :color="diagnosis.condition ? stateColors[diagnosis.condition.code] :'grey'"
          class="mx-2" />
        <span>{{ diagnosis.condition?.label }}</span>
      </p>
      <p>
        <span class="font-weight-bold">{{ $t('support.support-type') }}&nbsp;:</span><br>
        <v-chip v-if="diagnosis.pole_type.length>0" color="info" v-for="pt in diagnosis.pole_type" :key="pt.id"
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
    <v-card-actions>
      <v-spacer></v-spacer>
      <v-dialog max-width="500">
        <template v-slot:activator="{ props: activatorProps }">
          <v-btn v-bind="activatorProps" color="red" text="Supprimer" prepend-icon="mdi-delete-circle"></v-btn>
        </template>

        <template v-slot:default="{ isActive }">
          <v-card title="Suppression d'un diagnostic" color="red" prepend-icon="mdi-alert">
            <v-card-text>
              <div class="my-4">
              Vous êtes sur le point de supprimer un diagnostic, en êtes vous bien certain&nbsp;?
            </div>
              <v-btn color="white" block text="Oui, Supprimer" prepend-icon="mdi-delete-circle" @click="deleteDiag()"></v-btn>
            </v-card-text>

            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn text="Annuler" @click="isActive.value = false" prepend-icon="mdi-close-circle"></v-btn>
            </v-card-actions>
          </v-card>
        </template>
      </v-dialog>
      <v-btn color="orange" @click="updateDiag" prepend-icon="mdi-pencil-circle">Modifier</v-btn>
    </v-card-actions>
    <!-- <pre><code>{{ diagnosis }}</code></pre> -->
  </v-card>


</template>

<script setup>

const {diagnosis} = defineProps(['diagnosis'])
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


const updateDiag = () => {
  router.push({
    path: `/supports/${diagnosis.infrastructure}/diagnosis`,
    query: { modifyDiag: 'true', id_diagnosis: diagnosis.id }
  })
}

const deleteDiag = async () => {
  const deletedDiag = await useHttp(`/api/v1/cables/diagnosis/${diagnosis.id}/`, {method: 'delete'})
  console.log('deletedDiag',deletedDiag)
}

onMounted(()=>{
  console.log('diagnosis',diagnosis)
})

</script>
