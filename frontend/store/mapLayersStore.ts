/**
 * mapLayerStore to handle map layers loading
 */

import { defineStore } from "pinia";

export const useMapLayersStore = defineStore("mapLayers", {
  state: () => ({ baseLayers: [] as BaseLayer[] }),
  actions: {
    async getMapBaseLayers() {
      await $fetch("/api/v1/map-layers/baselayers/")
        .then((data) => {
          this.baseLayers = data;
        })
        .catch((error) => {
          console.error(error);
        });
      // try {
      //   // gather layers from DB to be loaded with map

      // } catch (err) {
      //   console.error('ERROR err', err)
      //   const error = {}
      //   if (err.toString().includes('404')) {
      //     error.code = errorCodes.nomenclature_not_found.code
      //     error.msg = $nuxt.$t(
      //       `error.${errorCodes.nomenclature_not_found.msg}`
      //     )
      //     // if nuxt error message contains substring 'conditions'
      //   }
      //   // commit("errorStore/setError", error, { root: true });
      //   // log out user as application may not be reliable as is
      //   // $nuxt.$auth.logout();
      // }
    },
  },
});

interface BaseLayer {
  id: number;
  url: string;
  name: string;
  attribution?: string;
  default: boolean | undefined;
}
