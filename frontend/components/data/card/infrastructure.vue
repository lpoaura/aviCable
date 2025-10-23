<template>
  <v-card   >
    <v-card-item prepend-icon="mdi-map-marker-circle">
    <template #title>
      <widgets-neutralized-status :data="data" :detail="true" class="m1-2 float-right" />
      <widgets-risk-level-status :data="data" class="m1-2 float-right" detail />
      {{ $t("display.context") }}
    </template>
    <template #subtitle>{{ $t("filledIn") }} {{ new Date(data.properties.timestamp_create).toLocaleString() }} par {{
      data.properties.created_by?.username || '?' }}</template>
      </v-card-item>
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
        <v-col v-if="lastDiag?.arming.length" cols="12">
          <p>Type de support</p>
          <!-- <pre>{{ lastDiag }}</pre> -->
          <v-chip-group>
            <v-chip v-for="pt in lastDiag?.arming" :key="pt.id">
              <pre>{{ pt.label }}</pre>
            </v-chip>
          </v-chip-group>
        </v-col>
      </v-row>
    </v-card-text>
    <v-card-actions>

      <v-btn color="green" prepend-icon="mdi-plus-circle"
        @click="router.push({ path: `/infrastructures/${data?.properties.id}/diagnosis`, query: { type: data.resourcetype } })">Diagnostic</v-btn>
      <v-btn color="green" prepend-icon="mdi-plus-circle"
        @click="router.push({ path: `/infrastructures/${data?.properties.id}/operation`, query: { type: data.resourcetype } })">Neutralisation</v-btn>
      <v-spacer />
      <v-btn color="orange"
        @click="router.push({ path: `/infrastructures/${data.properties.id}/infrastructure`, query: { type: data.resourcetype } })"><v-icon>mdi-pencil-circle</v-icon>
        Modifier</v-btn>
      <v-dialog v-model="deleteModal" max-width="500">
        <template #activator="{ props: activatorProps }">
          <v-btn v-bind="activatorProps" color="red" text="Supprimer" prepend-icon="mdi-delete-circle" />
        </template>

        <template #default="{ isActive }">
          <v-card title="Suppression d'un diagnostic" color="red" prepend-icon="mdi-alert">
            <v-card-text>
              <div class="my-4">
                Vous êtes sur le point de supprimer une infrastructure, en êtes vous bien certain&nbsp;? {{
                  `/cables/${data.resourcetype.toLowerCase()}s/${data.properties.id}/` }}
              </div>
              <v-btn color="white" block text="Oui, Supprimer" prepend-icon="mdi-delete-circle"
                @click="deleteInfrastructure()" />
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

<script lang="ts" setup>
const { data } = defineProps(['data'])

const router = useRouter()

const deleteModal = ref(false)

const notificationStore = useNotificationStore()
const globalStore = useGlobalStore()

const { refreshData } = storeToRefs(globalStore)

const lastDiag = computed(() => {
  return data?.properties.diagnosis.find(
    (action: { last: boolean }) =>
      action.last
  )
})

const deleteInfrastructure = async () => {
  await useApi(`/api/v1/cables/${data.resourcetype.toLowerCase()}s/${data.properties.id}/`, { method: 'DELETE' })
  deleteModal.value = false
  refreshData.value = true
  notificationStore.setInfo({
    type: 'success',
    msg: 'Infrastructure supprimée avec succès'
  })
  router.push('/search')
}

</script>
