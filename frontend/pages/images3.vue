<template>
  <v-container>
    <v-form ref="form" v-model="valid" lazy-validation>
      <v-file-input v-model="file" label="Upload File" accept="*" :rules="[rules.required]" @change="onFileChange" />
      <v-btn :disabled="!valid" @click="uploadFile">Upload</v-btn>
      <v-alert v-if="error" type="error">{{ error }}</v-alert>
      <v-alert v-if="success" type="success">{{ success }}</v-alert>
    </v-form>
  </v-container>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const file = ref<File | null>(null);
const files = ref<File[]>([]);
const valid = ref(false);
const error = ref<string | null>(null);
const success = ref<string | null>(null);
const rules = {
  required: (v: any) => !!v || 'File is required',
};

// const { $http } = useApi();

// const onFileChange = (event: Event) => {
//   const target = event.target as HTMLInputElement;
//   if (target.files) {
//     files.value = Array.from(target.files);
//   }
// };

const onFileChange = (newFile: File | null) => {
  const target = event.target as HTMLInputElement;
  if (target.files) {
    files.value = Array.from(target.files);
  }
  file.value = files.value[0];
  error.value = null; // Reset error on file change
  success.value = null; // Reset success message on file change
};

const uploadFile = async () => {
  if (!file.value) {
    error.value = 'Please select a file to upload.';
    return;
  }

  const formData = new FormData();
  // console.log('file.value', file.value)
  formData.append('storage', file.value);
  formData.append('date','2024-01-01')

  try {
    const response = await $fetch('/api/v1/media/', {
      method: 'post',
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      body: formData
    });
    success.value = 'File uploaded successfully!';
    console.log(response.data);
  } catch (err) {
    error.value = 'Failed to upload file. Please try again.';
    console.error(err);
  }
};
</script>

<style scoped>
/* Add any custom styles here */
</style>
