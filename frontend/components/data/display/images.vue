<template>
  <v-list lines="three">
    <v-list-item v-for="(item, index) in items" :title="item.title" :subtitle="item.remark" @click="modal = true">
      <template v-slot:prepend>
        <v-avatar color="grey-lighten-1" :rounded="false" :flat="true">
          <v-img :src="item.prependAvatar"></v-img>
        </v-avatar>
      </template>
      <template v-slot:append v-if="edit">
        <v-btn color="blue-lighten-1" icon="mdi-pencil" variant="text" size="small"></v-btn>
        <v-btn color="red-lighten-1" icon="mdi-trash-can" variant="text" size="small"
          @click="mediaStore.deleteMedia(index)"></v-btn>
      </template>
      <v-dialog v-if="!edit" :max-width="mobile ? '100%' : '70%'" v-model="modal">
        <template v-slot:default="{ isActive }">
          <v-card :title="item.id ? `#${item.id} ${item.date}` : item.date"
            :subtitle="([item.author, item.source]).join(', ')">
            <template v-slot:append>
              <v-icon color="primary" icon="mdi-close" @click="isActive.value = false"></v-icon>
            </template>
            <v-img :src="item.storage"></v-img>
            <v-card-text v-if="item.remark">
              {{ item.remark }}
            </v-card-text>
          </v-card>
        </template>
      </v-dialog>
    </v-list-item>
  </v-list>
</template>

<script lang="ts" setup>
import { useDisplay } from "vuetify";
import type { MediaData } from "~/types/media";

const { mobile } = useDisplay()

const { medias } = defineProps<{
  medias: MediaData[]; // Replace 'any' with the actual type of data if known
  edit: boolean;
}>();
const mediaStore = useMediaStore()
const modal = ref<boolean>(false)

const items = computed(() => medias.map((media: MediaData) => {
  return {
    prependAvatar: media.storage instanceof File ? URL.createObjectURL(media.storage) : media.storage,
    title: `${media.date} (${media.author || '-'} / ${media.source || '-'})`,
    subtitle: media.remark,
    ...media
  }
}))

</script>
