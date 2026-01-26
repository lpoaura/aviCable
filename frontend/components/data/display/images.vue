<template>
  <v-list lines="three">
    <v-list-item v-for="(item, index) in items" :title="item.title" :subtitle="item.remark">
      <template v-slot:prepend>
        <v-avatar color="grey-lighten-1" :rounded="false" :flat="true" @click="showModal(item)">
          <v-img :src="item.prependAvatar"></v-img>
        </v-avatar>
      </template>
      <template v-slot:append v-if="edit">
        <v-btn color="blue-lighten-1" icon="mdi-pencil" @click="selectMedia(index)" variant="text" size="small"></v-btn>
        <v-btn color="red-lighten-1" icon="mdi-trash-can" variant="text" size="small"
          @click="mediaStore.deleteMedia(index)"></v-btn>
      </template>

    </v-list-item>
    <v-dialog v-if="!edit && modalItem" :max-width="mobile ? '100%' : '70%'" v-model="modal">
      <template #default="{ isActive }">
        <v-card prepend-icon="mdi-camera"
          :title="!!modalItem.id ? `#${modalItem.id} ${format(modalItem.date, 'yyyy-MM-dd')}` : format(modalItem.date, 'yyyy-MM-dd')"
          :subtitle="([modalItem.author, modalItem.source]).join(', ')">
          <template v-slot:append>
            <v-icon color="primary" icon="mdi-close" @click="isActive.value = false"></v-icon>
          </template>
          <v-img :src="modalItem.storage"></v-img>
          <v-card-text v-if="modalItem.remark">
            {{ modalItem.remark }}
          </v-card-text>
        </v-card>
      </template>
    </v-dialog>
  </v-list>
</template>

<script lang="ts" setup>
import { useDisplay } from "vuetify";
import type { MediaData } from "~/types/media";
import { format } from 'date-fns'
const { mobile } = useDisplay()

const { medias, edit } = defineProps<{
  medias: MediaData[]; // Replace 'any' with the actual type of data if known
  edit: boolean;
}>();
const mediaStore = useMediaStore()
const modal = ref<boolean>(false)
const modalItem = ref<MediaData | null>(null)

const { selectedMedia } = storeToRefs(mediaStore)

const items = computed(() => medias.map((media: MediaData) => {
  const titleValues= []
  if(!media.id) {titleValues.push(`[new]`)}
  if (media.date) {titleValues.push(format(media.date, 'yyyy-MM-dd'))}
  titleValues.push(`(${media.author || '-'} / ${media.source || '-'})`)
  return {
    prependAvatar: media.storage instanceof File ? URL.createObjectURL(media.storage) : media.storage,
    title: titleValues.join(' '),
    subtitle: media.remark,
    ...media
  }
}))

const selectMedia = (index: number) => {
  console.debug('selectMedia event', index)
  selectedMedia.value = medias[index]
}

const showModal = (item: MediaData) => {
  modal.value = true
  modalItem.value = item
}

onUnmounted(() => {
  mediaStore.purgeSelectedMedia()
})

</script>
