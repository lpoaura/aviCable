<template>
  <v-row>
    <v-container>
      <v-card title="Photos" prepend-icon="mdi-camera">
        <data-display-images :medias="medias" :edit="true" />
        <v-divider></v-divider>
        <form-image v-if="editMedia" />
        <v-divider></v-divider>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn prepend-icon="mdi-camera-plus-outline" @click="editMedia = !editMedia" color="info">{{
            t('forms.newImage') }}</v-btn>
        </v-card-actions>
      </v-card>
    </v-container>
  </v-row>
</template>

<script lang="ts" setup>

import type { MediaData } from "~/types/media";

const { t } = useI18n()
// Define props with default values

// const medias = ref<FormData[]>([])
const mediaStore = useMediaStore()
const { medias, selectedMedia } = storeToRefs(mediaStore)

// const emit = defineEmits()

// const updateImage = (data: MediaData) => {
//   console.log('<updateImage> data type', data, typeof data, data instanceof FormData)
//   // if (data.id) {
//   //   medias.value[medias.value.findIndex(item => item.id === data.id)] = data
//   // } else {
//   //   medias.value.push(data)
//   // }
// }

const editMedia = ref(false)

// const items = computed(() => medias.value.map((media: MediaData) => {
//   return {
//     prependAvatar: URL.createObjectURL(media.storage),
//     title: `${media.date} (${media.author || '-'} / ${media.source || '-'})`,
//     subtitle: media.remark
//   }
// }))

// watch(items, async (newQuestion, oldQuestion) => {
//   console.log('watch items', newQuestion, oldQuestion)
// })

watch(
  () => selectedMedia.value,
  (newValue, _oldValue) => {
    editMedia.value = !!Object.keys(newValue).length
  },
)
</script>
