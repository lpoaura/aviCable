<template>
  <v-card class="my-2" :title="$t('display.mortalityCases')">
    <template v-for="(mortality, index) in data" #text :key="index" @click="dataDetail(mortality)">
      <div>
        <p> {{ index }} <v-tooltip :text="mortality.death_cause.label">
            <template #activator="{ props }">
              <v-icon :color="'red'">
                {{ deathCauseIcons[mortality.death_cause.code] || 'mdi-help' }}
              </v-icon>
            </template>
          </v-tooltip> <strong>{{ mortality.species.vernacular_name }}</strong> (<i>{{ mortality.species.scientific_name
            }}</i>)
          le {{ mortality.date }}
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
        <!-- <pre><code>{{ diagnosis }}</code></pre> -->
      </div>
    </template>
  </v-card>
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
