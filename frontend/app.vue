<template>
  <v-app id="inspire">

    <layout-drawer-menu />
    <layout-app-bar />

    <v-main>
      <NuxtLayout>
        <VitePwaManifest />
        <NuxtLoadingIndicator />
        <NuxtPage />
      </NuxtLayout>
    </v-main>
    <utils-error-snackbar centered />
    <ClientOnly>
      <div v-if="$pwa?.needRefresh" class="pwa-toast" role="alert">
        <div class="message">
          {{ $t('pwa.reloadNeeded') }}
        </div>
        <button v-if="$pwa.needRefresh" @click="$pwa.updateServiceWorker()">
          {{ $t('pwa.reload') }}
        </button>
        <button @click="$pwa.cancelPrompt()">
          {{ $t('pwa.close') }}
        </button>
      </div>
      <div v-if="$pwa?.showInstallPrompt && !$pwa?.offlineReady && !$pwa?.needRefresh" class="pwa-toast" role="alert">
        <div class="message">
          <span>
            {{ $t('pwa.installPwa') }}
          </span>
        </div>
        <button @click="$pwa.install()">
          {{ $t('pwa.install') }}
        </button>
        <button @click="$pwa.cancelInstall()">
          {{ $t('pwa.cancel') }}
        </button>
      </div>
    </ClientOnly>
  </v-app>
</template>

<script setup lang="ts">

import { onMounted } from 'vue'


const auth = useAuth()

const nomenclaturesStore = useNomenclaturesStore()
const mapLayersStore = useMapLayersStore()
const globalStore = useGlobalStore()
const { t } = useI18n()

const loadBaseMapLayers = () => {
  mapLayersStore.getMapBaseLayers()
}

const loadNomenclatures = () => {
  nomenclaturesStore.loadNomenclatures()
}

onMounted(() => {
  loadBaseMapLayers()
  loadNomenclatures()
  globalStore.setUserAvatar()
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
  background-color: rgba(255, 255, 255, 0.8);
}

.pwa-toast .message {
  margin-bottom: 8px;
}

.pwa-toast button {
  border: 1px solid grey;
  outline: none;
  margin-right: 5px;
  border-radius: 5px;
  padding: 3px 10px;
}
</style>
