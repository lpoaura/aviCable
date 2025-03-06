<template>
  <v-row class="pa-0 fill-height fluid">
    <v-col cols="12" lg="9">
      <v-row justify="center">
        <v-col cols="12" class="justify-center pa-10">
          <div class="text-h2 mb--1">
            <v-avatar size="80" image="/img/icon.png" rounded="0"/> {{ $t('app.appName') }}
          </div>
        </v-col>

      </v-row>
    </v-col>
    <v-col cols="12" lg="3" class="pa-0 ">
      <posts-list />
    </v-col>
  </v-row>
</template>

<script setup lang="ts">
useHead({
  title: 'aviCable - Home',
  meta: [
    { name: 'description', content: 'Home page' }
  ],
})
</script>
