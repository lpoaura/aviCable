<template>
  <v-container>
    <v-form ref="loginForm" v-model="valid" lazy-validation>
      <v-container>
        <v-row>
          <v-col cols="12">
            <v-file-input clearable accept="image/*" density="compact" :title="t('picture.dragAndDrop')" variant="solo"
              :rules="[rules.filesize]" @change="selectedFile($event)"></v-file-input>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12" md="4">
            <v-date-input v-model="date" :locale="currentLocale?.iso" :label="t('date')"
              inner-prepend-icon="mdi-calendar" variant="solo" density="compact" :rules="[rules.required]"
              :max="new Date()" required />
          </v-col>
          <v-col cols="12" md="4">
            <v-text-field v-model="author" :counter="100" :label="t('author')" required variant="solo"
              density="compact"></v-text-field>
          </v-col>
          <v-col cols="12" md="4">
            <v-text-field v-model="source" :counter="100" :label="t('source')" required variant="solo"
              density="compact"></v-text-field>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12">
            <v-textarea v-model="remark" :label="t('remark')" required variant="solo" density="compact"></v-textarea>
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
const date = ref<Date | null>(null)
const author = ref<string | null>(null)
const source = ref<string | null>(null)
const remark = ref<string | null>(null)



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
      !!date.value && formData.append('date', date.value.toISOString().substring(0, 10))
      !!author.value && formData.append('author', author.value)
      !!source.value && formData.append('source', source.value)
      !!remark.value && formData.append('remark', remark.value)
      console.log('formData', formData)
      // create Media
      const { data: newImg } = await useApi<Media>("/api/v1/media/", {
        method: 'post',
        body: formData
      })
      !!newImg.value && mediaIdList.push(newImg.value.id) // set Media id to mediaIdList
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
