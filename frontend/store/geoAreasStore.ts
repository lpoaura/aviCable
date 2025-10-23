// Nuxt Store module: cablesStore for Cables module
import { defineStore } from 'pinia'
import type { FeatureCollection } from 'geojson'
export const useGeoAreasStore = defineStore('geoAreas', {
  state: () => ({
    municipalities: {} as FeatureCollection, // Infrastructure data
    departements: {} as FeatureCollection,
    municipalitiesVisible: false,
    departmentsVisible: false,
    // pointData: {}, // Pole and Pylon data
    // lineData: {}, // Cable lines data
    controller: null as AbortController | null,
  }),
  actions: {
    async getMunicipalities(params: Object) {
      if (this.controller === null) {
        this.controller = new AbortController();
      }
      const { signal } = this.controller;
      console.debug('<getMunicipalities> this.controller', this.controller)
      try {
        params['type__code'] = "ADMIN_COM"
        console.debug("getMunicipalities signal", signal)
        await useApi(
          '/api/v1/geoareas/', { signal, params }
        ).then(resp => {
          console.debug('useApi municipalities datra',resp.data)
          this.municipalities = resp.data.value
        })
      } catch (error: any) {
        if (error instanceof Error && error.name === "AbortError") {
          console.debug("Requête annulée");
        } else {
          console.error(error);
        }
      } finally {
        // Reset loading status and controller
        this.controller = null; // Reset the controller after the request
      }

    },
    
    cancelRequest() {
      console.debug('cancelRequest abort request - 1', this.controller)
      this.controller?.abort()
      console.debug('cancelRequest abort request - 2', this.controller)
      this.controller = null;
      console.debug('cancelRequest abort request - 3', this.controller)
    },
  }
})
