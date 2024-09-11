<template>
  <v-card class="my-2" :title="$t('display.operation')">
    <template #subtitle>{{ $t("realizedOn") }} <strong>{{ operation.date }}</strong></template>
    <template #text>
      <div v-if="operation.remark"><strong>{{$t("app.remark")}}</strong>&nbsp;: {{ operation.remark }}
      </div>
      <div>
        <span class="font-weight-bold">
          {{ $t("operation.equipment", operation.equipments.length, {count: operation.equipments.length} )}}
        </span>
        <v-list lines="two">
          <v-list-item v-for="(equipment, index) in operation.equipments" :key="index">
            <template #title><v-chip>{{ equipment.type.code }} </v-chip> {{ equipment.type.label }} <strong>x{{
                equipment.count }}</strong>
            </template>
            <div v-if="equipment.reference"><strong>{{$t("reference")}}</strong>&nbsp;: {{ equipment.reference }}
            </div>
            <div v-if="equipment.comment"><strong>{{$t("app.remark")}}</strong>&nbsp;: {{ equipment.comment }}</div>
          </v-list-item>
        </v-list>
      </div>
    </template>
    <v-card-actions>
      <v-spacer />
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
      <v-btn color="orange" prepend-icon="mdi-pencil-circle" @click="updateDiag()">
        Modifier</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script setup lang="ts">

const {supportId, operation} = defineProps(['operation','supportId'])

const router = useRouter()
const emit = defineEmits()

const updateDiag = () => {
  router.push({
    path: `/infrastructures/${supportId}/operation`,
    query: { id_operation: operation.id }
  })
}

const deleteOperation = async () => {
  await useHttp(`/api/v1/cables/operations/${operation.id}/`, {method: 'delete'})
  emit('delete')
}
</script>
