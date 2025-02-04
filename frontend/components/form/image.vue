<template>
  <v-container>
    <v-form ref="loginForm" v-model="valid" lazy-validation>
      <v-container>
        <v-row>
          <v-col cols="12">
            <v-file-upload v-if="!selectedMedia.id" ref="fileInput" v-model="files" clearable accept="image/*" density="compact"
              :title="t('picture.dragAndDrop')" variant="solo" :rules="[rules.filesize]"
              @change="selectedFile($event)"></v-file-upload>
              <v-else>
                <v-img :src="selectedMedia.storage" max-height="200"></v-img>
              </v-else>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12" md="4">
            <v-date-input v-model="selectedMedia.date" :locale="currentLocale?.code" :label="t('date')" prepend-icon=""
              prepend-inner-icon="mdi-calendar" variant="solo" density="compact" :rules="[rules.required]"
              :max="new Date()" required />
          </v-col>
          <v-col cols="12" md="4">
            <v-text-field v-model="selectedMedia.author" :counter="100" :label="t('author')" required variant="solo"
              density="compact"></v-text-field>
          </v-col>
          <v-col cols="12" md="4">
            <v-text-field v-model="selectedMedia.source" :counter="100" :label="t('source')" required variant="solo"
              density="compact"></v-text-field>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12">
            <v-textarea v-model="selectedMedia.remark" :label="t('remark')" required variant="solo"
              density="compact"></v-textarea>
          </v-col>
        </v-row>
        <v-btn :disabled="!globalFormValid" :prepend-icon="globalFormValid ? 'mdi-check' : 'mdi-alert'" color="success"
          @click="addMedia">{{ t('forms.add') }}</v-btn>
      </v-container>
    </v-form>
  </v-container>
</template>

<script setup lang="ts">
import type { StoreGeneric } from 'pinia'
const { t, locales } = useI18n()

//const files = ref<FileList | null>([] as unknown as FileList)
const files = ref()
const fileInput = ref()
const valid = ref(false)
// const date = ref(new Date())

const mediaStore: StoreGeneric = useMediaStore()
const { selectedMedia } = storeToRefs(mediaStore)

const locale = useLocale()
const currentLocale = computed(() => locales.value.find(item => item.code == locale.value))

const rules = reactive({
  required: (v: string | number) => !!v || t('valid.required'),
  filesize: (v: any) => {
    // console.log('rules.filesize',!!selectedMedia.value.id, v[0], typeof v, Object.keys(v))
    (!v[0] || v[0].size < 20000000) || 'Avatar size should be less than 20 MB!'
  },
  textLength: (v: string) => (v || '').length <= 300 || `${t('valid.length')}: 300`,
})

const globalFormValid = computed(() => valid && (selectedMedia.value.id || !!files.value))

const selectedFile = (event: Event) => {
  console.log(event)
  const uploadedFiles = (<HTMLInputElement>event?.target).files
  if (!!uploadedFiles && uploadedFiles.length > 0) {
    selectedMedia.value.storage = uploadedFiles[0]
  } else {
    selectedMedia.value.storage = null
  }
}

const addMedia = () => {
  console.log('mediaStore', mediaStore)
  mediaStore.addSelectedToMedias()
  // mediaStore.resetSelectedMedia()
  mediaStore.purgeSelectedMedia()
  files.value = []
}

// watch(date, (newVal: Date, _oldVal) => {
//   selectedMedia.value.date = newVal.toISOString().substring(0, 10)
//   console.log('watch date', selectedMedia.value.date)
// })

watch(files,
  (newVal: Date, _oldVal) => {
    console.log('watch files', newVal)
  },
  { deep: true }
)
onMounted(() => {
  if (!selectedMedia.value.date) selectedMedia.value.date = mediaStore.date
})

</script>
