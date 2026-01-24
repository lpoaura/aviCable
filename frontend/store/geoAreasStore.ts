// Nuxt Store module: cablesStore for Cables module
import { defineStore } from 'pinia'
import type { FeatureCollection } from 'geojson'
import type { GeoAreaFeatureCollection , GeoAreasFetchParams} from '~/types/geoAreas';


export const useGeoAreasStore = defineStore('geoAreas', {
  state: () => ({
    municipalities: {} as GeoAreaFeatureCollection, // Infrastructure data
    departements: {} as GeoAreaFeatureCollection,
    municipalitiesVisible: false,
    departmentsVisible: false,
    // pointData: {}, // Pole and Pylon data
    // lineData: {}, // Cable lines data
    controller: null as AbortController | null,
  }),
  actions: {
    async getMunicipalities(params: GeoAreasFetchParams) {
      if (this.controller === null) {
        this.controller = new AbortController();
      }
      const { signal } = this.controller;
      console.debug('<getMunicipalities> this.controller', this.controller)
      try {
        params['type__code'] = "ADMIN_COM"
        console.debug("getMunicipalities signal", signal)
        await authStore.authedGet<GeoAreaFeatureCollection>(
          '/api/v1/geoareas/', { signal, params }
        ).then(resp => {
          console.debug('municipalities data', resp.data)
          if (resp.data.value) {
            this.municipalities = resp.data.value
          }
        })
      } catch (error: unknown ) {
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
