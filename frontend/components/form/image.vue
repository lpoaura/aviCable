<template>
  <v-container>
    <v-form ref="loginForm" v-model="valid" lazy-validation>
      <v-container>
        <v-row>
          <v-col cols="12">
            <v-file-upload clearable accept="image/*" density="compact" :title="t('picture.dragAndDrop')" variant="solo"
              :rules="[rules.filesize]" @change="selectedFile($event)"></v-file-upload>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12" md="4">
            <v-date-input v-model="data.date" :locale="currentLocale?.iso" :label="t('date')"
              inner-prepend-icon="mdi-calendar" variant="solo" density="compact" :rules="[rules.required]"
              :max="new Date()" required />
          </v-col>
          <v-col cols="12" md="4">
            <v-text-field v-model="data.author" :counter="100" :label="t('author')" required variant="solo"
              density="compact"></v-text-field>
          </v-col>
          <v-col cols="12" md="4">
            <v-text-field v-model="data.source" :counter="100" :label="t('source')" required variant="solo"
              density="compact"></v-text-field>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12">
            <v-textarea v-model="data.remark" :label="t('remark')" required variant="solo" density="compact"></v-textarea>
          </v-col>
        </v-row>

        <v-btn :disabled="!valid" color="success" @click="createNewMedia()">load images {{ valid ? 'OK' : 'NOK'
          }}</v-btn>
      </v-container>
    </v-form>
  </v-container>
</template>

<script setup lang="ts">
import type { Media } from '~/types/cables'
const { t, locales } = useI18n()

const files = ref([])
const valid = ref(false)
const data = reactive<Media>({
  date: (new Date()).toISOString(),
  author: null,
  source: null,
  remark: null,
  storage: null
})
// const date = ref<Date | null>(null)
// const author = ref<string | null>(null)
// const source = ref<string | null>(null)
// const remark = ref<string | null>(null)

const {media} = defineProps<{
  media?: number
}>()

const emit = defineEmits<{
  update: [value: FormData]
}>()

const locale = useLocale()
const currentLocale = computed(() => locales.value.find(item => item.code == locale.value))

const rules = reactive({
  required: (v: string | number) => !!v || t('valid.required'),
  filesize: (v: any) => {
    console.log('rules.filesize', v[0], typeof v, Object.keys(v))
    !v[0] || v[0].size < 20000000 || 'Avatar size should be less than 20 MB!'
  },
  textLength: (v: string) => (v || '').length <= 300 || `${t('valid.length')}: 300`,
})

const selectedFile = (event: Event) => {
  console.log(event)
  files.value = event?.target?.files
  console.log(typeof files.value)
}


const createNewMedia = async () => {
  const mediaIdList: number[] = []
  if (files.value.length > 0) {
    const file = files.value[0]
    try {
      const formData = new FormData()
      formData.append('storage', file) // fill-in FormData with img file
      // TODO get true date and other form fields below
      !!data.date && formData.append('date', data.date instanceof Date && data.date.toISOString().substring(0, 10) || data.date)
      !!data.author && formData.append('author', data.author)
      !!data.source && formData.append('source', data.source)
      !!data.remark && formData.append('remark', data.remark)
      console.log('formData', formData)
      emit('update', formData)
      // create Media
      // const { data: newImg } = await useApi<Media>("/api/v1/media/", {
      //   method: 'post',
      //   body: formData
      // })
      // !!newImg.value && mediaIdList.push(newImg.value.id) // set Media id to mediaIdList
    } catch (_err) {
      console.error(_err)
    }
  }

  console.log('mediaList', mediaIdList)

}

onMounted(() => {
  // if (!date.value) { date.value = new Date() }
})

</script>
