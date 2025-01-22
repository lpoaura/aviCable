<template>
  <v-row>
    <v-container>
      <v-card title="Photos">
        <v-list lines="three" selectable @click="test($event)">
          <v-list-item v-for="item in items" :title="item.title" :subtitle="item.remark">
            <template v-slot:prepend>
              <v-avatar color="grey-lighten-1" :rounded="false" :flat="true">
                <v-img :src="item.prependAvatar"></v-img>
              </v-avatar>
            </template>

            <template v-slot:append>
              <v-btn color="grey-lighten-1" icon="mdi-information" variant="text"></v-btn>
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

const medias = ref<FormData[]>([])

const { mediasList } = defineProps({
  mediaList: { type: Array<Media>, default: [] }
});

const emit = defineEmits()

const test = (event: FormData) => {
  console.log(event)
}

const updateImage = (data: FormData) => {
  console.log('<updateImage> data type', data, typeof data, data instanceof FormData)
  medias.value.push(data)
}

const editMedia = ref(false)

const items = computed(() => medias.value.map((media: FormData) => {
  console.log('media', media)
  const obj: Media = {} as Media;
  media.forEach((value, key) => (obj[key] = value));
  console.log('obj storage', obj?.storage)
  return {
    prependAvatar: URL.createObjectURL(obj?.storage),
    title: `${obj.date} (${obj.author || '-'} / ${obj.source || '-'})`,
    subtitle: obj.remark
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
