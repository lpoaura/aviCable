<template>
  <v-container class="fill-height pa-0" fluid>
    <v-card class="fill-height" width="100%">
      <slot />
    </v-card>
  </v-container>
</template>


<script setup lang="ts" >

onMounted(() => {
  console.log('mounted mayoyt')
  const authStore = useAuthStore()
  authStore.checkAuth()
  console.log('CHECK', authStore.isAuthenticated , !authStore.user ,!authStore.userInfo, authStore.isAuthenticated && !authStore.user && !authStore.userInfo)
  if (authStore.isAuthenticated && authStore.authTokens && (!authStore.user || !authStore.userInfo)) {
    console.log('fetchUser')
    // authStore.fetchUser()
  }
})

</script>