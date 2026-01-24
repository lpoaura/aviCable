<template>
  <v-container>
    <v-row align="center" id="partners" dense class="justify-center">
      <v-col v-for="i in partners" :key="i.id" loading sm="4" md="3" lg="2" class="pa-3">
        <v-tooltip bottom>
          <template v-slot:activator="{ props }">
            <a :href="i.url" target="_blank" v-bind="props">
              <!-- TODO: Retirer le string.replace  -->
              <v-img max-height="100" contain :src="i.logo.replace(':3000', ':8000')" :alt="i.name" :title="i.name" />
            </a>
          </template>
          <span>{{ i.name }}</span>
        </v-tooltip>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { useDisplay } from 'vuetify'
const { mobile } = useDisplay()
const config = useRuntimeConfig()
const { data: partners } = await useFetch(`${config.public.baseURL}/api/v1/custom-content/partners/`)
</script>

