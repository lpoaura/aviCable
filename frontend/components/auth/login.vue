<template>
  <v-sheet width="100%" max-width="600" class="mx-auto">
    <v-form ref="loginForm" v-model="valid" @keyup.enter="userLogin">

      <v-card class="mx-auto pa-12 pb-8" elevation="0" rounded="lg">

        <div class="text-subtitle-1 text-medium-emphasis">Account</div>

        <v-text-field density="compact" placeholder="Usename" prepend-inner-icon="mdi-account-outline" variant="outlined"
          v-model="login.username" :rules="nameRules" @keyup.enter="userLogin" autofocus></v-text-field>

        <div class="text-subtitle-1 text-medium-emphasis d-flex align-center justify-space-between">
          Password

          <a class="text-caption text-decoration-none text-blue" :href="'/account/reset'" rel="noopener noreferrer"
          >
            Forgot login password?</a>
        </div>

        <v-text-field :append-inner-icon="visible ? 'mdi-eye-off' : 'mdi-eye'" :type="visible ? 'text' : 'password'"
          density="compact" placeholder="Enter your password" prepend-inner-icon="mdi-lock-outline" variant="outlined"
          @click:append-inner="visible = !visible" v-model="login.password" :rules="pwdRules"></v-text-field>

        <v-btn block class="mb-8" color="blue" size="large" variant="flat" :loading="loading" :disabled="!valid"
          @click="userLogin()">
          {{ $t('login.sign-in') }}
        </v-btn>
        <!-- <v-card-text class="text-center">
          <a class="text-blue text-decoration-none" href="#" rel="noopener noreferrer" target="_blank">
            Sign up now <v-icon icon="mdi-chevron-right"></v-icon>
          </a>
        </v-card-text> -->
      </v-card>
    </v-form>
  </v-sheet>
</template>

<script setup type="ts">
import * as errorCodes from '~/static/errorConfig.json'
// import { useErrorsStore } from 'store/errorStore'

const { t } = useI18n()
const router = useRouter()


const errorStore = useErrorsStore()
const auth = useAuth()
// interface Login {
//   username: string,
//   password: string,
// }
const loginForm = ref(null)
const valid = ref(false)
const loading = ref(false)
const login = reactive({
  username: '',
  password: ''
})
const nameRules = reactive([v => !!v || t('login.required_username_msg')])
const pwdRules = reactive([v => !!v || t('login.required_pwd_msg')])
const visible = ref(false)

const error = ref(null)


const userLogin = async () => {
  // loading=true
  try {
    // check theform is validated
    if (valid) {
      console.log('Try Auth', login)
      await auth.loginWith('local', {
        body: login
      })
      router.push('/search')
    }
  } catch (err) {

    // if nuxt error message contains substring '401'
    if (err.toString().includes('401')) {
      error.value.code = errorCodes.authentication.code
      error.value.msg = t(`error.${errorCodes.authentication.msg}`)
    } else {
      // for other login errors
      error.value.code = errorCodes.login.code
      error.value.msg = t(`error.${errorCodes.login.msg}`)
    }
    // loading = false
    // set error message to errorStore and triggers message displyy through "err" watcher in
    // error-snackbar component
    errorStore.setError(error)
  }
}
</script>
