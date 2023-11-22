<template>
  <v-navigation-drawer expand-on-hover rail  class="bg-light-blue-darken-3" theme="dark">
    <v-list class="bg-orange-darken-2">
      <v-list-item
        :prepend-avatar="$auth.loggedIn ? 'https://randomuser.me/api/portraits/lego/7.jpg' : 'https://randomuser.me/api/portraits/lego/1.jpg'"
        :title="$auth.user?.username || 'Not connected'" :subtitle="$auth.user?.email || 'mail@dot.com'"></v-list-item>
    </v-list>
    <v-divider></v-divider>
    <v-list density="compact" nav>
      <v-list-item v-if="$auth.loggedIn" v-for="[icon, text, url, loggedIn] in links" :prepend-icon="icon" :title="text"
        :to="url"></v-list-item>
    </v-list>
    <template v-if="$auth.loggedIn" v-slot:append>
      <v-list density="compact" nav>
        <v-list-item v-if="$auth.loggedIn" link href="/api/admin/" prepend-icon="mdi-cogs" :title="t('nav.admin')"
          value="starred"></v-list-item>
      </v-list>
    </template>
  </v-navigation-drawer>
</template>
<script setup>

const $auth = useAuth()
const { t } = useI18n()
// const drawer=ref(true)
// const rail=ref(true)

useRouter()
const links = ref([
  ['mdi-home', t('nav.home_page'), '/', null],
  ['mdi-map-search', t('nav.application'), '/search', true],
  ['mdi-information', t('nav.about'), '/about', true]
]);
</script>
