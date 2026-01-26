import { useAuthStore } from '~/store/authStore'

export default defineNuxtPlugin(async () => {
  const auth = useAuthStore()
  auth.init()

  await auth.getValidAccessToken()
})