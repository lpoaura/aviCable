import { defineStore } from "pinia";
import type { Medias, Media, MediaData } from "~/types/media";

export const useMediaStore = defineStore("media", {
  state: () => ({
    medias: [] as Medias,
    selectedMedia: {} as MediaData,
    mediaToDelete: {} as MediaData,
   }),
   actions: {
    async postMedia(data : MediaData) {
      try {
        const formData = new FormData()
      formData.append('storage', data.storage) // fill-in FormData with img file
      // TODO get true date and other form fields below
      const date = (new Date(data.date)).toISOString().substring(0,10)
      !!date && formData.append('date', date)
      !!data.author && formData.append('author', data.author)
      !!data.source && formData.append('source', data.source)
      !!data.remark && formData.append('remark', data.remark)
        const {data: media } = await useApi<Media>("/api/v1/media/", );
        media.value && this.medias.push(media.value)
      } catch (error) {
        console.error(error);
      }
    },
    addSelectedToMedias() {
      console.log('addSelectedToMedias')
      this.medias.push({...this.selectedMedia})
      // this.resetSelectedMedia()
    },
    resetSelectedMedia() {
      this.selectedMedia = {} as MediaData
    },
    async deleteMedia(index: number | null) {
      console.log()
      if (this.mediaToDelete && this.mediaToDelete.id) {
        const {data: resp } = await useApi<Media>(`/api/v1/media/${this.mediaToDelete.id}`, {method: 'DELETE'});
      }
      !!index && this.medias.slice(index,1)
    }
  },
});
