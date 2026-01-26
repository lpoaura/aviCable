export default defineNuxtRouteMiddleware(async (to) => {
  const auth = useAuthStore()

  // Tentative de refresh silencieux si besoin
  await auth.getValidAccessToken()

  if (!auth.isAuthenticated) {
    return navigateTo({
      path: '/account/login',
      query: {
        redirect: to.fullPath
      }
    })
  }
})