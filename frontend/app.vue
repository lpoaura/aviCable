
<template>
  <v-app id="inspire">

    <utils-drawer-menu />

    <v-app-bar color="light-blue-darken-3">
      <v-toolbar-title>{{ $t('app.app-name') }}</v-toolbar-title>
      <v-spacer />
      <div v-if="!mdAndDown">
        {{ user ? user.username : $t('app.signin') }}
      </div>
      <v-btn v-if="$auth.loggedIn" icon="mdi-logout" class="mr-2" @click="$auth.logout()" />
      <v-btn v-if="!$auth.loggedIn" icon="mdi-login" @click="router.push('/account/login')" class="mr-2" />
    </v-app-bar>
    <v-main>
      <NuxtLayout>
        <VitePwaManifest />
        <NuxtLoadingIndicator />
        <NuxtPage />
      </NuxtLayout>
    </v-main>
    <utils-error-snackbar centered />
  </v-app>
</template>

<script setup lang="ts">

import { ref, onMounted } from 'vue'
import { useDisplay } from 'vuetify'
// import { useMapLayersStore } from './store/mapLayersStore'
// import { useNomenclaturesStore } from './store/nomenclaturesStore'

const { mdAndDown } = useDisplay()
const router = useRouter()
const { user } = useAuth()

const loadBaseMapLayers = () => {
  const mapLayersStore = useMapLayersStore()
  mapLayersStore.getMapBaseLayers()
}

const loadNomenclatures = () => {
  const nomenclaturesStore = useNomenclaturesStore()
  nomenclaturesStore.loadNomenclatures()
}

onMounted(() => {
  loadBaseMapLayers()
  loadNomenclatures()
})

</script>
