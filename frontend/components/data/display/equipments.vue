<template>
        <span class="font-weight-bold">
          {{ $t("operation.equipment", equipments.length, { count: equipments.length }) }}
        </span>
        <v-list lines="two">
          <v-list-item v-for="(equipment, index) in equipments" :key="index">
            <template #title><v-chip>{{ equipment.type?.code }} </v-chip> {{ equipment.type.label }} <strong>x{{
              equipment.count }}</strong>
            </template>
            <div v-if="equipment.reference"><strong>{{ $t("reference") }}</strong>&nbsp;: {{ equipment.reference }}
            </div>
            <div v-if="equipment.comment"><strong>{{ $t("remark") }}</strong>&nbsp;: {{ equipment.comment }}</div>
          </v-list-item>
        </v-list>
  </template>

<script setup lang="ts">
import type {Equipment} from '~/types/cables';

const {equipments} = defineProps<{
  equipments: Equipment[];
}>();
</script>
