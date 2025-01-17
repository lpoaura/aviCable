import { defineStore } from "pinia";

export const useMapLayersStore = defineStore("mapLayers", {
  state: () => ({ baseLayers: [] as BaseLayer[] }),
  actions: {
    async getMapBaseLayers() {
      try {
        const {data: baseLayers } = await useApi("/api/v1/map-layers/baselayers/");
        if (baseLayers && Array.isArray(baseLayers.value)) {
          this.baseLayers = baseLayers.value as BaseLayer[]; // Type assertion
        } else {
          console.error("Unexpected data format:", baseLayers, Array.isArray(baseLayers));
        }
      } catch (error) {
        console.error(error);
      }
    },
  },
});

interface BaseLayer {
  id: number;
  url: string;
  name: string;
  attribution?: string | undefined;
  default: boolean | undefined;
}
