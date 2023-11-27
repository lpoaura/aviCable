<template>
  <v-sheet>
    <v-file-input ref="pictInput" v-model="newImg" :rules="rules" hide-input accept="image/png, image/jpeg"
      prepend-inner-icon="mdi-camera" chips multiple :label="$t('picture.add_file')" @change="displayImage" variant="solo"
      density="compact"></v-file-input>
    <pre>{{ newImg }}</pre>
    <v-list>
      <v-list-item v-for="(img, index) in imgFileContent" :key="index">
        <v-row>
          <v-col>
            <v-img :src="img" max-height="100" max-width="166" class="ma-2" />
          </v-col>
          <v-col>date: {{ pictDate }}</v-col>
          <v-col></v-col>
          <v-col cols="1">
            <v-icon small color="red">mdi-trash-can</v-icon>
          </v-col>
        </v-row>
      </v-list-item>
    </v-list>
  </v-sheet>
</template>

<script setup lang="ts">
import * as errorCodes from '~/static/errorConfig.json'
import type { ErrorInfo } from '~/store/errorStore';

const errorStore = useErrorsStore()

const {diagId} = defineProps(['diagId'])
const {t} = useI18n()

const pictInput = ref()
const newImg = ref()
const pictDate = ref(new Date(Date.now() - new Date().getTimezoneOffset() * 60000)
    .toISOString()
    .substr(0, 10))
const imgFileContent = ref([])
const imgFileObject = ref([])
const showError = ref(false)
// TODO test validate and display message in snackbar if issue
const rules = reactive([
  (value: File[]) => {
    return !value || !value.length || value[0].size < 5000000 || t('Image size should be less than 5 MB!')
  },
],)

const displayImage = () => {
  try {
    if (newImg ) {
      const reader = new FileReader()
      reader.readAsDataURL(newImg.value)
      // event listener on successful loading,
      reader.addEventListener('load', () => {
        imgFileContent.push(reader.result) // file content push to array
        imgFileObject.push(newImg.value) // File object push to array
        pictInput.reset() // reset v-file-input
      })
    }
  } catch (_err) {
    console.error(_err)
    const error : ErrorInfo = {
      code: errorCodes.img_loading.code,
      msg: t(`error.${errorCodes.img_loading.msg}`)
    }
    errorStore.setError(error)
    // set error message to errorStore and triggers message display through "err" watcher in
    // error-snackbar component
    // this.$store.commit('errorStore/setError', error)
  }
}

interface Error {
  code: string,
  msg: string
}
</script>
