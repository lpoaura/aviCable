<template>
  <v-container id="post">
    <v-row>
      <v-col>
        <h1 class="text-h2 mb--1">{{ post.title }}</h1>
        <div class="text-caption mb-4">
          {{ new Date(post.timestamp_create).toString() }}
        </div>
        <div class="text-h6 mb-4">{{ post.intro }}</div>
        <div v-html="post.body"></div>

        <v-fab-transition>
          <v-btn v-show="!hidden" class="v-btn-back" color="pink" absolute dark bottom right fab @click="$router.back()">
            <v-icon>mdi-arrow-left</v-icon>
          </v-btn>
        </v-fab-transition>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
const route = useRoute()
definePageMeta({
  auth: true,
});

const authStore = useAuthStore()

const { data: post } = await authStore.authedGet(`/api/v1/custom-content/news/${route.params.id}`)
</script>

<style scoped>
#post .v-btn-back {
  bottom: 0;
  position: absolute;
  margin: 0 0 30px 16px;
}
</style>
