<template>
  <v-row>
    <v-col align-self="center" class="ma-5 pa-5" justify="center">
      <h1><v-icon>mdi-information-outline</v-icon> {{ $t('about.title') }} {{ $t('app.appName') }}</h1>
      <div>
        <p class="py-2">New internet application to monitor the risks of overhead cables for birdlife, based on historic <a
          href="https://github.com/PnVanoise/cables" target="_blank">"cable" app
        </a> originally developped by <a href="https://github.com/PnVanoise" target="_blank">Parc national de la
          Vanoise</a>.
        </p>
        <p class="py-2">
        The application has been developed by LPO Auvergne-Rhône-Alpes under 
        <a href="https://opensource.org/licenses/AGPL-3.0" target="_blank">GNU AGPLv3</a> license. 
        The source code is hosted and available on github.com&nbsp;:
        <a href="https://github.com/lpoaura/aviCable" target="_blank">https://github.com/lpoaura/aviCable</a>
        </p>
      </div>
    </v-col>
    <v-col cols="12">
      <partners-component />
    </v-col>
  </v-row>
</template>


<script setup lang="ts">
const { t } = useI18n()
useHead({
  title: `aviCable - ${t('About')}`,
  meta: [
    { name: 'description', content: 'Home page' }
  ],
})
</script>
