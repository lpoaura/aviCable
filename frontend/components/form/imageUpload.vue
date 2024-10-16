<template>
  <v-container>
    <v-file-input v-model="files" label="Upload Images" multiple accept="image/*" outlined @change="onFileChange" />

    <v-row>
      <v-col v-for="(image, index) in imagePreviews" :key="index" cols="4">
        <v-img :src="image" aspect-ratio="1" />
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts" setup>
import { ref, watch, defineProps, defineEmits } from 'vue';

// Define props to receive data from the parent component
const props = defineProps<{
  modelValue: string[];
}>();

const emit = defineEmits<{
  (e: 'update:modelValue', value: string[]): void;
}>();

const files = ref<File[]>([]);
const imagePreviews = ref<string[]>([]);

// Watch for changes in the modelValue prop and update local state
watch(() => props.modelValue, (newValue) => {
  imagePreviews.value = newValue;
});

// Function to handle file changes
const onFileChange = (event: Event) => {
  const target = event.target as HTMLInputElement;
  const selectedFiles = target.files;

  if (selectedFiles) {
    const newImagePreviews: string[] = []; // Array to hold new previews

    for (let i = 0; i < selectedFiles.length; i++) {
      const file = selectedFiles[i];
      const reader = new FileReader();

      reader.onload = (e) => {
        if (e.target?.result) {
          newImagePreviews.push(e.target.result as string);
          // Emit the updated images to the parent
          emit('update:modelValue', [...imagePreviews.value, ...newImagePreviews]);
        }
      };

      reader.readAsDataURL(file);
    }
  }
};
</script>

<style scoped>
.v-img {
  max-height: 200px;
  object-fit: cover;
}
</style>
