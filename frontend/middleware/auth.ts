export default defineNuxtRouteMiddleware(async () => {
  const auth = useAuthStore()

  // Tentative de refresh silencieux si besoin
  await auth.getValidAccessToken()

  if (!auth.isAuthenticated) {
    return navigateTo('/account/login')
  }
})