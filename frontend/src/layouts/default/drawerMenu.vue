<template>
  <v-navigation-drawer v-if="!mobile" expand-on-hover rail class="bg-light-blue-darken-3">
    <!-- <v-list class="bg-orange-darken-2">
      <v-list-item
        :prepend-avatar="$auth.loggedIn ? 'https://randomuser.me/api/portraits/lego/7.jpg' : 'https://randomuser.me/api/portraits/lego/1.jpg'"
        :title="$auth.user?.username || 'Not connected'" :subtitle="$auth.user?.email || 'mail@dot.com'"></v-list-item>
    </v-list> -->
    <v-divider></v-divider>
    <v-list density="compact" nav>
      <v-list-item prepend-icon="mdi-home" :title="'nav.home_page'" to="/"></v-list-item>
      <!-- <v-list-item v-show="$auth.loggedIn" v-for="[icon, text, url, loggedIn] in links" :prepend-icon="icon"
        :title="text" :to="url"></v-list-item> -->
    </v-list>
    <!-- <template v-if="$auth.loggedIn" v-slot:append>
      <v-list density="compact" nav>
        <v-list-item v-if="$auth.loggedIn" link href="/api/admin/" prepend-icon="mdi-cogs" :title="t('nav.admin')"
          value="starred"></v-list-item>
      </v-list>
    </template> -->
  </v-navigation-drawer>
  <v-bottom-navigation v-if="mobile" :elevation="5" grow density="default" class="text-light-blue-darken-3"
    theme="dark">
    <!-- <v-btn v-show="$auth.loggedIn" v-for="[icon, text, url, loggedIn] in links" :to="url"> -->
    <v-btn v-for="[icon, text, url, loggedIn] in links" :key="icon" :to="url">
      <v-icon>{{icon}}</v-icon>
      <span>{{text}}</span>
    </v-btn>
    <!-- <v-btn v-if="$auth.loggedIn" class="bg-orange-darken-2" to="/account">
      <v-icon>mdi-account-circle</v-icon>
      <span>{{$auth.user?.username}}</span>
    </v-btn> -->
  </v-bottom-navigation>
</template>
<script setup>
import   {ref} from 'vue'
import { useRouter } from 'vue-router'

import { useDisplay } from 'vuetify'
// const $auth = useAuth()
// const { t } = useI18n()
const { mobile} = useDisplay()
// const drawer=ref(true)
// const rail=ref(true)

useRouter()
const links = ref([
  ['mdi-map-search', 'nav.application', '/search', true],
  ['mdi-information', 'nav.about', '/about', true]
]);
</script>
