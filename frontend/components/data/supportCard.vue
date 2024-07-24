<template>
  <v-card title="Information contextuelle">
    <v-card-text>
      <v-row>
        <v-col cols="12" lg="6">
          <p class="text-strong" v-if="data.properties.geo_area.length > 0">
            Limites administratives
          </p>
          <v-chip-group>
            <v-chip v-for="(ga, index) in data.properties.geo_area" :key="index">
              {{ ga.name }} ({{ ga.code }})
            </v-chip>
          </v-chip-group>
        </v-col>
        <v-col cols="12" lg="6">
          <p v-if="data.properties.sensitive_area.length > 0">
            Zones sensibles
          </p>
          <v-chip-group>
            <v-chip v-for="sa in data.properties.sensitive_area" :key="sa.id">
              {{ sa.name }} {{ sa.name }}
            </v-chip>
          </v-chip-group>
        </v-col>
        <v-col cols="12" v-if="lastDiag && lastDiag.pole_type.length">
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

      <v-btn color="green" @click="router.push(`/supports/${data?.properties.id}/diagnosis`)"
        prepend-icon="mdi-plus-circle">Diagnostic</v-btn>
      <v-btn color="green" @click="router.push(`/supports/${data?.properties.id}/operation`)"
        prepend-icon="mdi-plus-circle">Neutralisation</v-btn>
      <v-spacer></v-spacer>
      <v-btn density="compact" color="orange"
        @click="$router.push(`/supports/${data.properties.id}/support`)"><v-icon>mdi-pencil-circle</v-icon>
        Modifier</v-btn>

    </v-card-actions>
  </v-card>
</template>

<script lang="ts" setup>
const {data} = defineProps(['data'])

const router = useRouter()

const lastDiag = computed(() => {
  return data?.properties.diagnosis.find(
        (action: { last: boolean }) =>
           action.last
      )
})

</script>
