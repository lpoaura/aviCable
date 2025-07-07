<template>
  <v-navigation-drawer v-if="!mobile || mobile" v-model="drawer" :rail="rail" class="bg-light-blue-darken-3"
    @click="rail = false">
    <v-list class="bg-orange-darken-2">
      <v-list-item
        :prepend-avatar="$auth.loggedIn ? `https://randomuser.me/api/portraits/lego/${userAvatar}.jpg` : 'https://randomuser.me/api/portraits/lego/1.jpg'"
        :title="$auth.user?.username || 'Not connected'" :subtitle="$auth.user?.email || 'mail@dot.com'">
        <template #append>
          <v-btn icon="mdi-chevron-left" variant="text" @click.stop="rail = !rail" />
        </template>
      </v-list-item>
    </v-list>
    <v-divider />
    <v-list density="compact" nav>
      <v-list-item prepend-icon="mdi-home-outline" :title="t('nav.home_page')" to="/" />
      <v-list-item v-for="[icon, text, url] in links" v-if="$auth.loggedIn" :prepend-icon="icon" :title="text"
        :to="url" />
      <v-list-item prepend-icon="mdi-information-outline" :title="t('nav.about')" to="/about" />
    </v-list>
    <template v-if="$auth.loggedIn" #append>
      <v-list density="compact" nav>
        <v-list-item v-if="$auth.loggedIn" link href="/api/admin/" prepend-icon="mdi-cogs" :title="t('nav.admin')"
          value="starred" />
        <v-list-item v-if="mobile"> <v-btn icon="mdi-chevron-left" variant="text"
            @click.stop="drawer = !drawer" /></v-list-item>
      </v-list>
    </template>
  </v-navigation-drawer>
</template>
<script setup>
import { useDisplay } from 'vuetify'
const $auth = useAuth()
const { t } = useI18n()
const { mobile } = useDisplay()

useRouter()
const links = ref([
  ['mdi-map-search', t('nav.application'), '/search']
]);

const rail = ref(true)
const globalStore = useGlobalStore()
const { drawer, userAvatar } = storeToRefs(globalStore)

</script>
