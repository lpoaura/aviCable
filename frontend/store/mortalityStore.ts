/**
 * mapLayerStore to handle map layers loading
 */

import { defineStore } from "pinia";
import type { FeatureCollection, Feature } from "geojson";

import { useCoordinatesStore } from "./coordinatesStore";

export const useMortalityStore = defineStore("mortality", {
  state: () => ({
    mortalityData: {} as FeatureCollection,
    mortalityItem: {} as Feature,
  }),
  getters: {
    // // get FeatureCollection data
    // infstrData(state) {
    //   return state.infstrData
    // },
    // get FeatureCollection array containing data (Json Object)
    getMortalityFeatures(state) {
      return state.mortalityData.features;
    },
    getMortalityItem(state) {
      return state.mortalityItem;
    },
  },
  actions: {
    async getMortalityData (params : { [key: string]: string }, controller: AbortController) {
      try {
        const data = await $http.$get("/api/v1/mortality/", {signal: controller.signal, params});
        this.mortalityData = data;
      } catch (error) {
        console.error(error);
      }
    },
    setMortalityItem(data) {
      this.mortalityItem = data;
    },
  },
});

interface MortalityData {
  properties: {
    id: number;
    vernacular_name: string;
    scientific_name: string;
    death_cause?: string;
    default: boolean | undefined;
  };
}
