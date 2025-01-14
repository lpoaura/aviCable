<template>
  <v-container>
    <v-file-upload clearable v-model="loadedImages" accept="image/*" density="compact"
      title="Glisser/déposer votre fichier" variant="solo"></v-file-upload>
    <v-date-input v-model="date" :locale="currentLocale?.iso" label="Date de visite" inner-prepend-icon="mdi-calendar"
      variant="solo" density="compact" :rules="[rules.required]" :max="new Date()" required />
    <v-text-field v-model="author" :counter="100" label="Autheur" required variant="solo"
      density="compact"></v-text-field>
    <v-text-field v-model="source" :counter="100" label="Source" required variant="solo"
      density="compact"></v-text-field>
    <v-textarea v-model="remark" label="Source" required variant="solo" density="compact"></v-textarea>
    <v-btn color="success" @click="createNewMedia()">load images</v-btn>
  </v-container>
</template>
<script setup lang="ts">

const { t, locales } = useI18n()

const loadedImages = ref([])
const date = ref<Date | null>(null)
const author = ref<string | null>(null)
const source = ref<string | null>(null)
const remark = ref<string | null>(null)

const locale = useLocale()
const currentLocale = computed(() => locales.value.find(item => item.code == locale.value))

const rules = reactive({
  required: (v: string | number) => !!v || t('valid.required'),
  textLength: (v: string) => (v || '').length <= 300 || `${t('valid.length')}: 300`,
})

const createNewMedia = async () => {
  const mediaIdList: number[] = []
  // await all Promises be resolved before returning result
  await Promise.all(
    // upc for "util-picture-component": task on each img file of the map
    loadedImages.value.map(async (img) => {
      console.log('img', img)
      try {
        const formData = new FormData()
        formData.append('storage', img) // fill-in FormData with img file
        // TODO get true date and other form fields below
        formData.append('date', date.value.toISOString().substring(0, 10))
        formData.append('author', author.value)
        formData.append('source', source.value)
        formData.append('remark', remark.value)
        console.log('formData', formData)
        // create Media
        const { data: newImg } = await useHttp("/api/v1/media/", {
          method: 'POST',
          body: formData
        })
        console.log('newImg', newImg)
        mediaIdList.push(newImg.value.id) // set Media id to mediaIdList
      } catch (_err) {
        console.error(_err)
      }
    })
  )
  console.log('mediaList', mediaIdList)
}

onMounted(() => {
  if (!date.value) { date.value = new Date() }
})

</script>
