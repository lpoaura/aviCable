<template>
  <v-sheet width="100%" max-width="600" class="mx-auto">
    <v-form ref="loginForm" v-model="formValid" @keyup.enter="userLogin">

      <v-card class="mx-auto pa-12 pb-8" elevation="0" rounded="lg">

        <div class="text-subtitle-1 text-medium-emphasis">Account</div>

        <v-text-field v-model="login.username" density="compact" placeholder="Usename"
          prepend-inner-icon="mdi-account-outline" variant="outlined" :rules="nameRules" autofocus
          @keyup.enter="userLogin" />

        <div class="text-subtitle-1 text-medium-emphasis d-flex align-center justify-space-between">
          Password

        </div>

        <v-text-field v-model="login.password" :append-inner-icon="visible ? 'mdi-eye-off' : 'mdi-eye'"
          :type="visible ? 'text' : 'password'" density="compact" placeholder="Enter your password"
          prepend-inner-icon="mdi-lock-outline" variant="outlined" :rules="pwdRules"
          @click:append-inner="visible = !visible" />

        <v-btn block class="mb-8" color="blue" size="large" variant="flat" :loading="loading" :disabled="!formValid"
          @click="userLogin()">
          {{ $t('login.sign-in') }}
        </v-btn>
        <div>
          <NuxtLink class="text-caption text-decoration-none text-blue" to="/account/signup">{{ $t('login.sign-up') }} ?
          </NuxtLink>
          <v-spacer />
          <!-- <NuxtLink class="text-caption text-decoration-none text-blue" to="/account/reset">{{
            $t('login.forgotten-password') }}?</NuxtLink> -->
        </div>
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
const { t } = useI18n()
const router = useRouter()

const authStore = useAuthStore()
const notificationStore = useNotificationStore()

const formValid = ref(false)
const loading = ref(false)
const login = reactive({
  username: '',
  password: ''
})
const nameRules = reactive([v => !!v || t('login.required_username_msg')])
const pwdRules = reactive([v => !!v || t('login.required_pwd_msg')])
const visible = ref(false)

// const nomenclaturesStore = useNomenclaturesStore()

const userLogin = async () => {
  try {
    if (formValid.value) {
      console.log('authStore', authStore)
      await authStore.login(login)
      // nomenclaturesStore.loadNomenclatures()
      notificationStore.setInfo({
        type: 'success',
        msg: `You successfully logged in`
      })
      router.push('/search')
    }
  } catch (err) {
    console.error('Login Error', err.data.data.detail)
    const message = err.data?.data?.detail || err
    notificationStore.setInfo({
      type: 'error',
      msg: message
    })
  }
}
</script>
