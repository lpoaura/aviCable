import { defineStore, acceptHMRUpdate } from "pinia";
import type { Medias, Media, MediaData } from "~/types/media";
import { errorStore } from ".";
import { useRuntimeConfig } from "#app";

const config = useRuntimeConfig()
// const {$http} = useNuxtApp()

export const useMediaStore = defineStore("media", {
  state: () => ({
    medias: [] as Medias,
    selectedMedia: {} as MediaData,
    mediaToDelete: {} as MediaData,
    date: null as Date|null,
  }),
  actions: {
    async postMedia(media: MediaData) {
      console.log('postMedia before post/update', media);
      const formData = new FormData();
      const date = !!media.date && (new Date(media.date)).toISOString().substring(0, 10);

      if (date) {
        formData.append('date', date);
      }

      console.log('media.storage', media.storage, media.storage instanceof File, typeof media.storage);

      if (media.storage instanceof File) {
        console.debug('<postMedia> media.storage', media.storage)
        formData.append('storage', media.storage); // fill-in FormData with img file
      }
      if (media.author) {
        formData.append('author', media.author);
      }
      if (media.source) {
        formData.append('source', media.source);
      }
      if (media.remark) {
        formData.append('remark', media.remark);
      }
      console.debug('<postMedia> media', media)
      const url = config.public.baseURL + `/api/v1/media/${media.id ? `${media.id}/` : ''}`
      console.debug('<postMedia> API Urls', config.public.baseUrl, url)
      const newImg: Media = await $fetch<Media>(url, {
        method: media.id ? 'patch' : 'post',
        body: formData
      });

      // if (error.value) {
      //   console.error('Error posting media:', error.value);
      //   throw new Error('Failed to post media');
      // }

      console.log('postMedia response', newImg); // Log the entire response
      return newImg.id; // Return the ID
    },
    async postMedias() {
      return Promise.all(this.medias.map(media => this.postMedia(media)))
    },
    addSelectedToMedias() {
      console.log('addSelectedToMedias')
      if (this.selectedMedia.id) {
        this.medias[this.medias.findIndex(item => item.id === this.selectedMedia.id)] = this.selectedMedia
      } else {
        this.medias.push(this.selectedMedia)
      }
      // this.resetSelectedMedia()
    },
    purgeSelectedMedia() {
      this.selectedMedia = {} as MediaData
    },
    resetSelectedMedia() {
      this.selectedMedia = {
        date: this.date,
        author: this.medias[0]?.author,
        source: this.medias[0]?.source,
        storage: null,
      }
    },
    resetMedias() {
      this.medias = [] as Medias
      this.date = null
    },
    async deleteMedia(index: number) {
      console.log('deleteMedia', index, this.medias, this.medias[index])
      try {
        this.mediaToDelete = this.medias[index]
        const file = { ...this.mediaToDelete }
        console.log('this.mediaToDelete test', (index !== null), this.mediaToDelete, this.mediaToDelete.id)
        if (this.mediaToDelete && this.mediaToDelete.id) {
          const { data: _resp } = await useApi<Media>(`/api/v1/media/${this.mediaToDelete.id}`, { method: 'DELETE' });
        }
        this.medias.splice(index, 1)
        errorStore.err = {
          code: 123,
          msg: `Photo ${file.storage} - ${file.date} successfully deleted`
        }
      } catch (error) {
        errorStore.err = {
          code: 123,
          msg: `Delete photo failed : ${error}`
        }
      }
    }
  },
});


if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useMediaStore, import.meta.hot))
}