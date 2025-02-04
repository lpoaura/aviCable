<template>
  <v-row>
    <v-col align-self="center" class="ma-5 pa-5" justify="center">
      <h1>{{ $t('about.title') }} {{ $t('app.appName') }}</h1>
      <div>
        New internet application to monitor the risks of overhead cables for birdlife, based on historic <a
          href="https://github.com/PnVanoise/cables" target="_blank">"cable" app
        </a> originally developped by <a href="https://github.com/PnVanoise" target="_blank">Parc national de la
          Vanoise</a>.

      </div>
    </v-col>
  </v-row>
</template>


<script setup lang="ts">
const {t} = useI18n()
useHead({
  title: `aviCable - ${t('About')}`,
  meta: [
    { name: 'description', content: 'Home page' }
  ],
})
</script>
