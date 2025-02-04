<template>
  <v-row>
    <v-container>
      <v-card :title="t('Equipments')" prepend-icon="mdi-camera">
        <data-display-equipments :equipments="equipments" :edit="true" />
        <v-divider></v-divider>
        <form-equipment v-if="edit" />
        <v-divider></v-divider>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn prepend-icon="mdi-camera-plus-outline" @click="edit = !edit" color="info">{{
            t('forms.Equipment') }}</v-btn>
        </v-card-actions>
      </v-card>
    </v-container>
  </v-row>
</template>

<script lang="ts" setup>
import type {Equipment} from '~/types/cables'


const { t } = useI18n()

const {equipments} = defineProps<{
  equipments: Equipment[],
}>()

const edit = ref(false)

</script>
