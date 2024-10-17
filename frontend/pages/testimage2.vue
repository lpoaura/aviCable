<template>
  <v-container>
    <v-file-input v-model="files" multiple label="Upload Images" accept="image/*" @change="onFileChange" />
    <v-btn :disabled="!files.length" @click="uploadImages">Upload</v-btn>
    <v-list>
      <v-list-item-group>
        <v-list-item v-for="(file, index) in files" :key="index">
          <v-list-item-content>{{ file.name }}</v-list-item-content>
        </v-list-item>
      </v-list-item-group>
    </v-list>
  </v-container>
</template>

<script lang="ts" setup>
const files = ref<File[]>([]);

const onFileChange = (event: Event) => {
  const target = event.target as HTMLInputElement;
  if (target.files) {
    files.value = Array.from(target.files);
  }
};

const uploadImages = async () => {
  const url = '/api/v1/media/'
  const formData = new FormData();
  files.value.forEach((file) => {
    formData.append('storage', file);
  });

  try {
    const response = await useHttp(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'multipart/form-data'
        },
        body: formData
      })
    console.log('Upload successful:', response.data);
  } catch (error) {
    console.error('Error uploading images:', error);
  }
};
</script>

<style scoped>
/* Add any styles you need here */
</style>
