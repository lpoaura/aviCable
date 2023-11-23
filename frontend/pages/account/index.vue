<script setup lang="ts">
import { useDisplay } from 'vuetify'

definePageMeta({ middleware: 'auth' })
const reveal = ref(false)
const { user, loggedIn } = useAuth()
const {mobile} = useDisplay()
</script>

<template>
  <v-container>
    <div v-if="loggedIn && user">
      <div>{{ user.email }}</div>
      <p class="text-h4 text--primary">
        {{ user.username }}
      </p>
      <p>{{ user.first_name }} {{ user.last_name }}</p>
    </div>
    <div v-if="$auth.loggedIn">
      <v-btn @click="$auth.logout()">
        <v-icon>mdi-logout</v-icon>{{$t('logout')}}
      </v-btn>
    </div>
  </v-container>
</template>
