<template>
  <template  v-for="(mortality, index) in data" :key="index" @click="dataDetail(mortality)">
    <v-card class="my-2" prepend-icon="mdi-coffin">
      <template #title><strong>{{ mortality.date }}</strong> - {{ $t('display.mortalityCases') }}</template>
      <template #subtitle>{{ $t("filledIn") }} {{ new Date(mortality.timestamp_create).toLocaleString() }} par {{
        mortality.created_by?.username || '?' }}</template>
      <template #text>
        <div>
          <p><strong>Espèce</strong>&nbsp;: <strong>{{ mortality.species.vernacular_name }}</strong> (<i>{{
            mortality.species.scientific_name
          }}</i>)
            le {{ mortality.date }} par {{ mortality.observer }}
          </p>
          <p><strong>Cause</strong>&nbsp;: <v-tooltip :text="mortality.death_cause.label">
              <template #activator="{ props }">
                <v-icon :color="'red'">
                  {{ deathCauseIcons[mortality.death_cause.code] || 'mdi-help' }}
                </v-icon> {{ mortality.death_cause.label }}
              </template>
            </v-tooltip>
          </p>
          <p v-if="mortality.comment">
            <span class="font-weight-bold">{{ $t('remark') }}</span>
          </p>
          <p>
            {{ mortality.comment }}
          </p>
          <v-list>
            <v-list-item v-for="img in mortality.media" :key="img.id">
              <v-row>
                <v-col>
                  <v-img :src="img.storage" max-height="100" max-width="166" class="ma-2" />
                </v-col>
              </v-row>
            </v-list-item>
          </v-list>
        </div>
      </template>
      <v-card-actions>
        <v-spacer />
        <v-btn color="info"
          @click="router.push({ path: `/mortality/${mortality.id}`})"><v-icon>mdi-eye</v-icon>
          Voir la donnée</v-btn>
      </v-card-actions>

    </v-card>
  </template>
</template>

<script setup lang="ts">

interface Props {
  data: object,
}
const router = useRouter()

const { data } = defineProps<Props>()

const deathCauseIcons = ref({
  COD_EL: 'mdi-lightning-bolt',
  COD_IM: 'mdi-star',
  COD_UNKNOWN: 'mdi-help'
})

const deleteItem = async () => {
  await useApi(`/api/v1/cables/mortality/${data.id}/`, { method: 'delete' })
  emit('delete')
}

const dataDetail = (data) => {
  router.push(`mortality/${data.id}`)
}


</script>
