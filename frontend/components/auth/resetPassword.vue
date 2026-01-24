<template>
  <v-sheet width="100%" max-width="600" class="mx-auto">
    <v-form ref="loginForm" v-model="valid" @keyup.enter="userResetPassword">

      <v-card class="mx-auto pa-12 pb-8" elevation="0" rounded="lg">

        <div class="text-subtitle-1 text-medium-emphasis">Reset password</div>

        <v-text-field density="compact" placeholder="Email" prepend-inner-icon="mdi-account-outline" variant="outlined"
          v-model="reset.email" :rules="emailRules" @keyup.enter="userResetPassword" autofocus></v-text-field>

        <v-btn block class="mb-8" color="blue" size="large" variant="flat" :loading="loading" :disabled="!valid"
          @click="userResetPassword()">
          {{ $t('auth.resetPassword') }}
        </v-btn>

        <v-snackbar :timeout="2000" color="success" v-model="successMessage">
          {{ $t('auth.resetPasswordRequestSent') }}
        </v-snackbar>
        <!-- <v-card-text class="text-center">
            <a class="text-blue text-decoration-none" href="#" rel="noopener noreferrer" target="_blank">
              Sign up now <v-icon icon="mdi-chevron-right"></v-icon>
            </a>
          </v-card-text> -->
      </v-card>
    </v-form>

  </v-sheet>
</template>

<script setup lang="ts">
import type { NotificationInfo } from '~/types/notifications'

// import { useNotificationStore } from 'store/notificationStore'

const { t } = useI18n()
const router = useRouter()


const notificationStore = useNotificationStore()
const successMessage = ref(null)
const valid = ref(false)
const loading = ref(false)

const reset = reactive({
  email: ''
})

const emailRules = reactive([v => /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test(v) || t('auth.invalidEmail')])

const error: Reactive<NotificationInfo> = reactive<NotificationInfo>(null)


const userResetPassword = async () => {
  // loading=true
  try {
    // check theform is validated
    if (valid) {
      await useFetch('/api/v1/auth/users/reset_password/', { method: 'post', body: reset })
      notificationStore.setInfo({
        type: 'success',
        msg: t('auth.resetPasswordRequestSent')
      })
    }
  } catch (err) {
    console.error(err)
    const error: NotificationInfo = {
      type: 'error',
      msg: err.toString()
    }
    // if nuxt error message contains substring '401'
    notificationStore.setInfo(error)
  }
}
</script>
