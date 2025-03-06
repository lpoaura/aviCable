<template>
  <v-app-bar color="light-blue-darken-3" :density="mobile ? 'compact' : 'default'">
    <v-app-bar-nav-icon variant="text" @click.stop="drawer = !drawer" />
    <v-toolbar-title><v-avatar  image="/img/icon.png" rounded="0"/>  {{ $t('app.appShortName') }}</v-toolbar-title>
    <v-spacer />
    <div v-if="!mobile">
      {{ $auth.user?.username || 'Not connected' }}
    </div>
    <v-btn v-if="$auth.loggedIn" icon="mdi-logout" class="mr-2" @click="$auth.logout()" />
    <v-btn v-if="!$auth.loggedIn" icon="mdi-login" class="mr-2" @click="router.push('/account/login')" />
  </v-app-bar>
</template>

<script setup lang="ts">
import { useDisplay } from 'vuetify'
const { mobile } = useDisplay()
const router = useRouter()
const globalStore = useGlobalStore()
const { drawer } = storeToRefs(globalStore)
</script>
