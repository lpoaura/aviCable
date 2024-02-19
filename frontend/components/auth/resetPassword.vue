<template>
    <v-sheet width="100%" max-width="600" class="mx-auto">
      <v-form ref="loginForm" v-model="valid" @keyup.enter="userResetPassword">
  
        <v-card class="mx-auto pa-12 pb-8" elevation="0" rounded="lg">
  
          <div class="text-subtitle-1 text-medium-emphasis">Reset password</div>
  
          <v-text-field density="compact" placeholder="Email" prepend-inner-icon="mdi-account-outline" variant="outlined"
            v-model="reset.email" :rules="emailRules" @keyup.enter="userResetPassword" autofocus></v-text-field>
  

          <v-btn block class="mb-8" color="blue" size="large" variant="flat" :loading="loading" :disabled="!valid"
            @click="userResetPassword()">
            {{ $t('login.sign-in') }}
          </v-btn>
          <v-snackbar
      :timeout="2000"
      color="success"
      variant="outlined"
      v-model="successMessage"
    >

      message
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
  import type { ErrorInfo } from '~/store/errorStore'
  import * as errorCodes from '~/static/errorConfig.json'
  
  // import { useErrorsStore } from 'store/errorStore'
  
  const { t } = useI18n()
  const router = useRouter()
  
  
  const errorStore = useErrorsStore()
  const auth = useAuth()
  const loginForm = ref(null)
  const successMessage = ref(null)
  const valid = ref(false)
  const loading = ref(false)
  const reset = reactive({
    email: ''
  })
  const emailRules = reactive([v => /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(v) || t('login.required_username_msg')])
  
  const error : Reactive<ErrorInfo> = reactive<ErrorInfo>(null)
  
  
  const userResetPassword = async () => {
    // loading=true
    try {
      // check theform is validated
      if (valid) {
        successMessage.value = await useHttp('/api/v1/auth/users/reset_password/', {method: 'post', body: reset})
        
        // router.push('/')
      }
    } catch (err) {
        console.error(err)
        const error : ErrorInfo = {
            code: 'err',
            msg: err.toString()
        }
      // if nuxt error message contains substring '401'
      errorStore.setError(error)
    }
  }
  </script>
  