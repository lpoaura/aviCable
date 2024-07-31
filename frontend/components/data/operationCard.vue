<template>
  <v-card class="my-2" :title="$t('display.operation')" :subtitle="`${$t('operation.last-one')} ${operation.date}`">
    <template #text>
      <p>
        <span class="font-weight-bold">{{ $t('operation.type') }}</span>
        {{ operation.operation_type?.label }}
      </p>
      <p v-if="operation.equipments.length>0">
        <span class="font-weight-bold">{{ $t('operation.eqmt-type') }}</span>
        <v-chip v-for="et in operation.eqmt_type" :key="et.id">
          {{ et.label}}
        </v-chip>
      </p>
      <p v-if="operation.remark">
        <span class="font-weight-bold">{{ $t('app.remark') }}</span>
        {{ operation.remark }}
      </p>
      <div v-if="operation.equipments">
        <span class="font-weight-bold">Equipements&nbsp;: </span>
        <p v-for="(equipment, index) in operation.equipments" :key="index">
          -&nbsp;{{ equipment.type.label }} x{{ equipment.count }}
        </p>
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
