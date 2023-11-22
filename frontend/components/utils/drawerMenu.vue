<template>
  <v-navigation-drawer v-model="drawer" :rail="rail" permanent @click="rail = false" theme="dark">
    <v-list-item :prepend-avatar="'https://randomuser.me/api/portraits/men/85.jpg'"
      :title="$auth.user?.username || 'Not connected'" nav to="/account/">
      <template v-slot:append>
        <v-btn v-if="!rail" variant="text" icon="mdi-chevron-left" @click.stop="rail = !rail"></v-btn>
      </template>
    </v-list-item>

    <VDivider></VDivider>

    <VList>
      <VListItem v-if="$auth.loggedIn" v-for="[icon, text, url, loggedIn] in links" :key="icon" link :to="url">
        <template v-slot:prepend>
          <VIcon :icon="icon"></VIcon>
        </template>
        <VListItemTitle>{{ text }}</VListItemTitle>
      </VListItem>
      <VListItem v-if="!$auth.loggedIn" link to="/account/login">
        <template v-slot:prepend>
          <VIcon icon="mdi-login"></VIcon>
        </template>
        <VListItemTitle>login</VListItemTitle>
      </VListItem>
    </VList>
  </v-navigation-drawer>
</template>
<script setup>

const $auth = useAuth()
const { t } = useI18n()
const drawer=ref(true)
const rail=ref(true)

useRouter()
const links = ref([
  ['mdi-home', t('nav.home_page'), '/', null],
  ['mdi-map-search', t('nav.application'), '/search', true],
  ['mdi-cogs', t('nav.admin'), '/api/admin', true],
  ['mdi-information', t('nav.about'), '/about', true]
]);
</script>
