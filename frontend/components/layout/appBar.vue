<template>
    <v-app-bar color="light-blue-darken-3" :density="mobile ? 'compact': 'default'">
        <v-toolbar-title>{{ $t('app.app-name') }}</v-toolbar-title>
        <v-spacer />
        <div v-if="!mobile">
            {{ $auth.user?.username || 'Not connected' }}
        </div>
        <v-btn v-if="$auth.loggedIn" icon="mdi-logout" class="mr-2" @click="$auth.logout()" />
        <v-btn v-if="!$auth.loggedIn" icon="mdi-login" @click="router.push('/account/login')" class="mr-2" />
    </v-app-bar>
</template>

<script setup lang="ts">
import  {useDisplay} from 'vuetify'
const {mobile} = useDisplay()
const router = useRouter()
</script>