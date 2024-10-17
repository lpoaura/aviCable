<template>
  <v-container>
    <form-image-upload v-model="loadedImages" />
    <pre><code>{{ loadedImages }}</code></pre>
    <v-btn color="success" @click="createNewMedia()">load images</v-btn>
  </v-container>
</template>
<script setup lang="ts">

const loadedImages = ref([])

const createNewMedia =   async () => {
  const mediaIdList = []
  // await all Promises be resolved before returning result
  await Promise.all(
    // upc for "util-picture-component": task on each img file of the map
    loadedImages.value.map(async (img) => {
      try {
        const formData = new FormData()
        formData.append('storage', img) // fill-in FormData with img file
        // TODO get true date and other form fields below
        formData.append('date', '2022-01-01')
        formData.append('author', 'Bob')
        formData.append('source', 'LPO')
        formData.append('remark', 'Nothing to report')
        // console.log('formData',formData)
        // create Media
        const {data: newImg} = await useHttp("/api/v1/media/", {
          method: 'POST',
          headers: {
            'Content-Type': 'multipart/form-data'
          },
          body: formData
        })
        console.log('newImg',newImg)
        mediaIdList.push(newImg.value.id) // set Media id to mediaIdList
      } catch (_err) {
    console.error(_err)
      }
    })
  )
  console.log('mediaList', mediaIdList)
}

</script>
