<template>
  <v-row>
    <v-container>
      <v-card title="Photos" prepend-icon="mdi-camera">
        <data-display-images :medias="medias" :edit="true" />
        <v-divider></v-divider>
        <form-image v-if="edit" />
        <v-divider></v-divider>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn prepend-icon="mdi-camera-plus-outline" @click="edit = !edit" color="info">{{
            t('forms.newImage') }}</v-btn>
        </v-card-actions>
      </v-card>
    </v-container>
  </v-row>
</template>

<script lang="ts" setup>

const { t } = useI18n()

const mediaStore = useMediaStore()
const { medias, selectedMedia } = storeToRefs(mediaStore)

const edit = ref(false)

watch(
  () => selectedMedia.value,
  (newValue, _oldValue) => {
    edit.value = !!Object.keys(newValue).length
  },
)
</script>
