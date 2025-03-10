<template>
  <v-card title="Information contextuelle">
    <template #subtitle>{{ $t("filledIn") }} <strong>{{ new Date(item.properties.timestamp_create).toLocaleDateString() }}</strong> par {{ item.properties.created_by?.username || '?' }}</template>
    <v-card-text>
      <v-row>
        <v-col cols="12">
          <p v-if="item.properties.areas.length > 0" class="text-strong">
            <strong>Limites administratives</strong>
          </p>
          <v-chip-group>
            <v-chip v-for="(ga, index) in item.properties.areas" :key="index">
              {{ ga.name }} ({{ ga.code }})
            </v-chip>
          </v-chip-group>
        </v-col>
        <v-col v-if="item.properties.infrstr" cols="12">
          <p class="text-strong">
            <strong>Infrastructure</strong>
          </p>
          <v-chip-group>
            <v-chip :color="item.properties.infrstr.type== 1 ? 'success':'info'" :to="`/infrastructures/${item.properties.infrstr.id}`">
              {{ item.properties.infrstr.owner.label }} ({{ item.properties.infrstr.id }})
            </v-chip>
          </v-chip-group>
        </v-col>
        <v-col cols="12">
          <p><span class="font-weight-bold">Espèce&nbsp;:</span> {{ item.properties.species.vernacular_name }}
            (<i>{{ item.properties.species.scientific_name }} </i>)</p>
          <p>
            <span class="font-weight-bold">Nombre&nbsp;:</span> {{ item.properties.nb_death ? item.properties.nb_death :
              'x'
            }}
          </p>
          <p>
            <span class="font-weight-bold">Date&nbsp;:</span>
            {{ item.properties.date }}
          </p>
          <p>
            <span class="font-weight-bold">Observateur&nbsp;:</span>
            {{ item.properties.author }}
          </p>
          <p>
            <span class="font-weight-bold">Cause de mortalité&nbsp;:</span>
            <v-icon :color="'red'">
              {{ deathCauseIcons[item.properties?.death_cause.code] || 'mdi-help' }}
            </v-icon> {{ value }} {{ item.properties.death_cause.label }}
          </p>
          <p>
            <span class="font-weight-bold">Source de la donnée&nbsp;:</span>
            {{ item.properties.data_source ? item.properties.data_source : '-' }}
          </p>
          <data-display-images v-if="item.properties.media.length > 0" :edit="false" :medias="item.properties.media" />
        </v-col>
      </v-row>
    </v-card-text>
    <v-card-actions>
      <v-spacer />
      <v-btn color="orange" prepend-icon="mdi-pencil-circle" @click="updateDiag">Modifier</v-btn>
      <v-dialog v-model="deletedDiagConfirm" max-width="500">
        <template #activator="{ props: activatorProps }">
          <v-btn v-bind="activatorProps" color="red" text="Supprimer" prepend-icon="mdi-delete-circle" />
        </template>

        <template #default="{ isActive }">
          <v-card title="Suppression d'un diagnostic" color="red" prepend-icon="mdi-alert">
            <v-card-text>
              <div class="my-4">
                Vous êtes sur le point de supprimer un diagnostic, en êtes vous bien certain&nbsp;?
              </div>
              <v-btn color="white" block text="Oui, Supprimer" prepend-icon="mdi-delete-circle" @click="deleteData()" />
            </v-card-text>

            <v-card-actions>
              <v-spacer />
              <v-btn text="Annuler" prepend-icon="mdi-close-circle" @click="isActive.value = false" />
            </v-card-actions>
          </v-card>
        </template>
      </v-dialog>
    </v-card-actions>
  </v-card>
</template>

<script setup lang="ts">

const { itemId, item } = defineProps(['itemId', 'item'])

const router = useRouter()

const emit = defineEmits()
const deathCauseIcons = ref({
  COD_EL: 'mdi-lightning-bolt',
  COD_IM: 'mdi-star',
  COD_UNKNOWN: 'mdi-help'
})

const deletedDiagConfirm = ref(false)
const mediaStore = useMediaStore()
// const { medias } = storeToRefs(mediaStore)
const updateDiag = () => {
  router.push({
    path: `/mortality`,
    query: { id_mortality: itemId }
  })
}


const deleteData = async () => {
  await useApi(`/api/v1/mortality/${itemId}/`, { method: 'delete' })
  deletedDiagConfirm.value = false
  router.push("/search")
  emit('delete')
}
</script>
