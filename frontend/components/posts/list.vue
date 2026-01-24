<template>
  <v-sheet class="fill-height" dark align-self="start">

    <v-timeline side="end" align="start">
      <v-timeline-item :dot-color="post.private ? 'pink' : 'green'" size="small" v-for="post in posts" :key="post.id"
        :to="`/posts/${post.id}`">
        <template v-slot:icon>
          <v-icon size="x-small">{{ post.private ? 'mdi-lock' : '' }}</v-icon>
        </template>
        <div class="d-flex">

          <div @click="router.push(`/posts/${post.id}`)" class="pointer">
            <strong><small>{{ new Date(post.timestamp_create).toISOString().substr(0, 10) }}</small> {{ post.title
              }}</strong>
            <div class="text-caption">
              {{ post.intro }}
            </div>
          </div>
        </div>
      </v-timeline-item>

    </v-timeline>
  </v-sheet>
</template>

<script setup lang="ts">
const router = useRouter()

const authStore = useAuthStore()

const { data: posts } = await authStore.authedGet('/api/v1/custom-content/news/')
</script>


<style>
.pointer {
  cursor: pointer;
}
</style>
