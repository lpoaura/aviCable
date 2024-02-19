<template>
  <v-card class="my-2">
    <v-layout>
      <v-app-bar density="compact" color="blue-grey-lighten-4">
        <v-app-bar-title>
          {{ $t('display.operation') }}
        </v-app-bar-title>
        <v-spacer />
        <v-btn-toggle rounded="0" density="compact">
          <v-btn class="mr-2" v-if="operation.last" color="green" density="compact" icon="mdi-eye-plus-outline" />
          <v-btn class="mr-2" variant="elevated" density="compact" icon="mdi-pencil" color=orange
            @click="$router.push(`/supports/21/operation/${props.operation.id}`)" />
        </v-btn-toggle>
      </v-app-bar>
      <v-main>
        <v-card-subtitle class="ma-2">
          {{ $t('operation.last-one') }}{{ props.operation.date }}
        </v-card-subtitle><v-card-text>
          <p>
            <span class="font-weight-bold">{{ $t('operation.type') }}</span>
            {{ props.operation.operation_type.label }}
          </p>
          <p v-if="operation.equipments.length>0">
            <span class="font-weight-bold">{{ $t('operation.eqmt-type') }}</span>
            <v-chip v-for="et in operation.eqmt_type" :key="et.id">
              {{
              et.label
              }}
            </v-chip>
          </p>
          <p v-if="operation.remark">
            <span class="font-weight-bold">{{ $t('app.remark') }}</span>
            {{ operation.remark }}
          </p>
        </v-card-text>
      </v-main>
    </v-layout>
  </v-card>
</template>

<script setup lang="ts">

const props = defineProps(['operation'])
console.log('OPERATION', props.operation)
</script>
