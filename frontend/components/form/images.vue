<template>
  <v-row>
    <v-container>
      <v-card title="Photos">
        <v-list lines="three">
          <v-list-item v-for="(item,index) in items" :title="item.title" :subtitle="item.remark">
            <template v-slot:prepend>
              <v-avatar color="grey-lighten-1" :rounded="false" :flat="true">
                <v-img :src="item.prependAvatar"></v-img>
              </v-avatar>
            </template>
            <template v-slot:append>
              <v-btn color="blue-lighten-1" icon="mdi-pencil" variant="text" size="small"></v-btn>
              <v-btn color="red-lighten-1" icon="mdi-trash-can" variant="text" size="small" @click="mediaStore.deleteMedia(index)"></v-btn>
            </template>
          </v-list-item>
        </v-list>


        <v-divider></v-divider>
        <form-image v-if="editMedia" @update="updateImage($event)"></form-image>
        <v-divider></v-divider>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="editMedia = !editMedia" color="info">Add image</v-btn>
        </v-card-actions>

      </v-card>

    </v-container>
  </v-row>

</template>

<script lang="ts" setup>

import type { Media } from "~/types/cables";

const { t } = useI18n()
// Define props with default values

// const medias = ref<FormData[]>([])
const mediaStore = useMediaStore()
const { medias, selectedMedia } = storeToRefs(mediaStore)

const emit = defineEmits()

const test = (event: FormData) => {
  console.log(event)
}

const updateImage = (data: FormData) => {
  console.log('<updateImage> data type', data, typeof data, data instanceof FormData)
  medias.value.push(data)
}

const editMedia = ref(false)

const items = computed(() => medias.value.map((media: MediaData) => {
  // console.log('media', media)
  // const obj: Media = {} as Media;
  // media.forEach((value, key) => (obj[key] = value));
  // console.log('obj storage', obj?.storage)
  return {
    prependAvatar: URL.createObjectURL(media.storage),
    title: `${media.date} (${media.author || '-'} / ${media.source || '-'})`,
    subtitle: media.remark
  }
}))

watch(items, async (newQuestion, oldQuestion) => {
  console.log('watch items', newQuestion, oldQuestion)
})

watch(
  () => medias,
  (newValue, _oldValue) => {
    console.log('medias watcher', newValue.value)
    emit('update', newValue.value)
  },
  { deep: true }
)
</script>
