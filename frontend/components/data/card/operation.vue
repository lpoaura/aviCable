<template>
  <v-card class="my-2" :title="$t('display.neutralization')">
    <template #subtitle>{{ $t("realizedOn") }} <strong>{{ operation.date }}</strong></template>
    <v-card-text>
      <div>
        <span class="font-weight-bold">Niveau de neutralisation</span>&nbsp;: {{operation.neutralization_level === 'full' ? 'Totale': 'Partielle'}}
      </div>
      <div>
        <span class="font-weight-bold">
          {{ $t("operation.equipment", operation.equipments.length, { count: operation.equipments.length }) }}
        </span>
        <v-list lines="two">
          <v-list-item v-for="(equipment, index) in operation.equipments" :key="index">
            <template #title><v-chip>{{ equipment.type.code }} </v-chip> {{ equipment.type.label }} <strong>x{{
              equipment.count }}</strong>
            </template>
            <div v-if="equipment.reference"><strong>{{ $t("reference") }}</strong>&nbsp;: {{ equipment.reference }}
            </div>
            <div v-if="equipment.comment"><strong>{{ $t("remark") }}</strong>&nbsp;: {{ equipment.comment }}</div>
          </v-list-item>
        </v-list>
      </div>
      <div v-if="operation.remark"><strong>{{ $t("remark") }}</strong>&nbsp;: {{ operation.remark }}
      </div>
    </v-card-text>
    <data-display-images v-if="operation.media.length > 0" :edit="false" :medias="operation.media" />
    <v-card-actions>
      <v-spacer />
      <v-btn color="orange" prepend-icon="mdi-pencil-circle" @click="updateDiag()">
        Modifier</v-btn>
      <v-dialog max-width="500">
        <template #activator="{ props: activatorProps }">
          <v-btn v-bind="activatorProps" color="red" text="Supprimer" prepend-icon="mdi-delete-circle" />
        </template>

        <template #default="{ isActive }">
          <v-card title="Suppression d'une opération de neutralisation" color="red" prepend-icon="mdi-alert">
            <v-card-text>
              <div class="my-4">
                Vous êtes sur le point de supprimer une opération, en êtes vous bien certain&nbsp;?
              </div>
              <v-btn color="white" block text="Oui, Supprimer" prepend-icon="mdi-delete-circle"
                @click="deleteOperation()" />
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

const { supportId, operation, infrastructureType } = defineProps(['operation', 'supportId','infrastructureType'])

const router = useRouter()
const emit = defineEmits()

const updateDiag = () => {
  router.push({
    path: `/infrastructures/${supportId}/operation`,
    query: { id_operation: operation.id, type: infrastructureType }
  })
}

const deleteOperation = async () => {
  await useApi(`/api/v1/cables/operations/${operation.id}/`, { method: 'delete' })
  emit('delete')
}
</script>
