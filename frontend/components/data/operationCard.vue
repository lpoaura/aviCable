<template>
  <v-card class="my-2" :title="$t('display.operation')"
    :subtitle="`${$t('operation.last-one')} ${props.operation.date}`">
    <template v-slot:text>
      <p>
        <span class="font-weight-bold">{{ $t('operation.type') }}</span>
        {{ props.operation.operation_type.label }}
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
    <template v-slot:actions>
      <v-btn color="orange"
        @click="$router.push(`/supports/${supportId}/operation?id_operation=${props.operation.id}`)"><v-icon>mdi-pencil</v-icon>
        Modifier</v-btn>
    </template>
  </v-card>
</template>

<script setup lang="ts">

const props = defineProps(['operation','supportId'])
console.log('OPERATION', props.operation)
</script>
