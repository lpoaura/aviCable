import { defineStore } from "pinia";

export const useMapLayersStore = defineStore("mapLayers", {
  state: () => ({ baseLayers: [] as BaseLayer[] }),
  actions: {
    async getMapBaseLayers() {
      const baseLayers = await api.get<BaseLayer[]>("/api/v1/map-layers/baselayers/");
      console.log()
      if (baseLayers && Array.isArray(baseLayers)) {
        this.baseLayers = baseLayers as BaseLayer[]; // Type assertion
      } else {
        console.error("Unexpected data format:", baseLayers, Array.isArray(baseLayers));
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
