<template>
  <v-container>
    <v-row>
      <v-col align-self="center" class="ma-5 pa-5" justify="center" cols="12">
        <h1><v-icon>mdi-information-outline</v-icon> {{ $t('about.title') }} {{ $t('app.appName') }}</h1>
        <div>
          <p class="py-2">
            L'application <strong>aviCable</strong> (« Avifaune & Câbles ») facilite la collecte de données sur la
            mortalité aviaire, permet un suivi précis et actualisé de l'état des lignes et aide à identifier les poteaux
            électriques et les lignes électriques dangereux dans toute la France. De plus, cette application apporte une
            aide précieuse à la coordination des efforts de réduction des risques entre les différentes parties
            prenantes
            et comprend des rapports sur les visites régulières des sites, les diagnostics des lignes électriques et les
            détails des travaux de modernisation prévus ou réalisés.
          </p>
          <p class="py-2">
            L'application a été initialement développée par le <a href="https://github.com/PnVanoise"
              target="_blank">Parc
              national de la
              Vanoise</a>, dans le cadre de son accord
            avec Enedis et le département de la Savoie, puis étendue à la Haute-Savoie grâce au projet LIFE Gyphelp en
            2015. En 2016, cette initiative a été étendue à l'ensemble des Alpes du Nord avec la participation de divers
            acteurs locaux, tels que les parcs nationaux, les parcs régionaux, les départements, la LPO locale, Enedis,
            etc.</p>
          <p align="center">
            <a href="https://opensource.org/licenses/AGPL-3.0" target="_blank"><img class="ma-5" :height="50"
                src="https://upload.wikimedia.org/wikipedia/commons/0/06/AGPLv3_Logo.svg" /></a>
            <a href="https://github.com/lpoaura/aviCable" target="_blank"><img :height="50" class="ma-5"
                src="https://upload.wikimedia.org/wikipedia/commons/9/91/Octicons-mark-github.svg" /></a>
          </p>
        </div>
      </v-col>
      <v-col cols="6">

      </v-col>
      <v-col cols="6">

      </v-col>
      <v-col cols="12">
        <partners-component />
      </v-col>
    </v-row>
  </v-container>
</template>


<script setup lang="ts">
const { t } = useI18n()

// definePageMeta({
//   middleware: 'guest',
// })

useHead({
  title: `aviCable - ${t('About')}`,
  meta: [
    { name: 'description', content: 'Home page' }
  ],
})
</script>
