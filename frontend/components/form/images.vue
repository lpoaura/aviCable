<template>
  <v-row>
    <v-container>
      <v-list :items="items" lines="three" item-props selectable @click="test($event)">
      </v-list>
      <v-btn @click="editMedia = !editMedia">Add image</v-btn>
      <form-image @update="updateImage($event)"></form-image>
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

const test = (event) => {
  console.log(event)
}

const updateImage = (event) => {
  console.log('<updateImage>', event)
  medias.value.push(event)
}

const editMedia = ref(false)

const items = computed(() => medias.value.map((media: FormData) => {
  console.log('media', media)
  const obj: Media = {};
  media.forEach((value, key) => (obj[key] = value));
  console.log('obj storage', obj?.storage)

  return {
    prependAvatar: obj?.storage,
    title: `${obj.date} - ${obj.source}`,
    subtitle: obj.remark
  }
}))

watch(items, async (newQuestion, oldQuestion) => {
  console.log('watch items', newQuestion, oldQuestion)
})

watch(medias, (value) => {
  console.log('update medias', value)
  emit(`update`, value)
})

</script>
