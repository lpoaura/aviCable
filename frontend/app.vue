
<template>
  <v-app id="inspire">

    <utils-drawer-menu />

    <v-app-bar color="light-blue-darken-3" :density="mobile ? 'compact': 'default'">
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
    <ClientOnly>
      <div v-if="$pwa?.offlineReady || $pwa?.needRefresh" class="pwa-toast" role="alert">
        <div class="message">
          <span v-if="$pwa.offlineReady">
            App ready to work offline
          </span>
          <span v-else>
            New content available, click on reload button to update.
          </span>
        </div>
        <button v-if="$pwa.needRefresh" @click="$pwa.updateServiceWorker()">
          Reload
        </button>
        <button @click="$pwa.cancelPrompt()">
          Close
        </button>
      </div>
      <div v-if="$pwa?.showInstallPrompt && !$pwa?.offlineReady && !$pwa?.needRefresh" class="pwa-toast" role="alert">
        <div class="message">
          <span>
            Install PWA
          </span>
        </div>
        <button @click="$pwa.install()">
          Install
        </button>
        <button @click="$pwa.cancelInstall()">
          Cancel
        </button>
      </div>
    </ClientOnly>
  </v-app>
</template>

<script setup lang="ts">

import { ref, onMounted } from 'vue'
import { useDisplay } from 'vuetify'
// import { useMapLayersStore } from './store/mapLayersStore'
// import { useNomenclaturesStore } from './store/nomenclaturesStore'

const { mdAndDown , mobile } = useDisplay()
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



<style>
.pwa-toast {
  position: fixed;
  right: 0;
  bottom: 0;
  margin: 16px;
  padding: 12px;
  border: 1px solid #8885;
  border-radius: 4px;
  z-index: 1;
  text-align: left;
  box-shadow: 3px 4px 5px 0 #8885;
}

.pwa-toast .message {
  margin-bottom: 8px;
}

.pwa-toast button {
  border: 1px solid #8885;
  outline: none;
  margin-right: 5px;
  border-radius: 2px;
  padding: 3px 10px;
}
</style>