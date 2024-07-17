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
    </template>
    <template v-slot:actions>
      <v-btn v-if="operation.last" color="green" @click="newDiag"><v-icon>mdi-eye-plus</v-icon> Nouveau</v-btn>
      <v-btn color="orange"
        @click="$router.push(`/supports/${supportId}/operation/${props.operation.id}`)"><v-icon>mdi-pencil</v-icon>
        Modifier</v-btn>
    </template>
  </v-card>
</template>

<script setup lang="ts">

const props = defineProps(['operation','supportId'])
console.log('OPERATION', props.operation)
</script>
