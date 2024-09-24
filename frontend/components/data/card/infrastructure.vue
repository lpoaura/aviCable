<template>
  <v-card>
    <template #title>
      Information contextuelle
      <widgets-neutralized-status :data="data" :detail="true" class="m1-2 float-right" />
      <widgets-risk-level-status :data="data" class="m1-2 float-right" detail />
    </template>
    <v-card-text>
      <v-row>
        <v-col cols="12">
          <p v-if="data.properties.areas.length > 0" class="text-strong">
            Limites administratives
          </p>
          <v-chip-group>
            <v-chip v-for="(ga, index) in data.properties.areas" :key="index">
              {{ ga.name }} ({{ ga.code }})
            </v-chip>
          </v-chip-group>
        </v-col>
        <v-col v-if="lastDiag?.pole_type.length" cols="12">
          <p>Type de support</p>
          <!-- <pre>{{ lastDiag }}</pre> -->
          <v-chip-group>
            <v-chip v-for="pt in lastDiag?.pole_type" :key="pt.id">
              <pre>{{ pt.label }}</pre>
            </v-chip>
          </v-chip-group>
        </v-col>
      </v-row>
    </v-card-text>
    <v-card-actions>

      <v-btn color="green" prepend-icon="mdi-plus-circle"
        @click="router.push({ path: `/infrastructures/${data?.properties.id}/diagnosis`, query: {type:data.resourcetype}})">Diagnostic</v-btn>
      <v-btn color="green" prepend-icon="mdi-plus-circle"
        @click="router.push(`/infrastructures/${data?.properties.id}/operation`)">Neutralisation</v-btn>
      <v-spacer />
      <v-btn color="orange"
        @click="router.push({path:`/infrastructures/${data.properties.id}/infrastructure`, query: {type:data.resourcetype}})"><v-icon>mdi-pencil-circle</v-icon>
        Modifier</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script lang="ts" setup>
const {data} = defineProps(['data'])

const router = useRouter()

const lastOp : boolean = computed(() => {
  return data?.properties.operations?.length > 0 ? data?.properties.operations[0] : null
})

const neutralized : boolean = computed(() => {
  return data?.properties.operations.length>0
})



const lastDiag = computed(() => {
  return data?.properties.diagnosis.find(
        (action: { last: boolean }) =>
           action.last
      )
})

</script>
