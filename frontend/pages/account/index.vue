<script setup lang="ts">
import { useDisplay } from 'vuetify'

definePageMeta({ middleware: 'auth' })

const authStore = useAuthStore()
const user = computed(() => authStore.userInfo)
const loggedIn = computed(() => authStore.isAuthenticated)

</script>

<template>
  <v-container>
    <div v-if="loggedIn && authStore.userInfo">
      <div>{{ user.email }}</div>
      <p class="text-h4 text--primary">
        {{ user.username }}
      </p>
      <p>{{ user.first_name }} {{ user.last_name }}</p>
    </div>
    <div v-if="loggedIn">
      <v-btn @click="authStore.logout()">
        <v-icon>mdi-logout</v-icon>{{$t('logout')}}
      </v-btn>
    </div>
  </v-container>
</template>
