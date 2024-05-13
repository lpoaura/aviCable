<template>
  <v-app>
    <default-bar />
<default-menu />
    <default-view />
  </v-app>
</template>

<script lang="ts" setup>
  import DefaultBar from './AppBar.vue'
  import DefaultView from './View.vue'
  import DefaultMenu from './drawerMenu.vue'
</script>
