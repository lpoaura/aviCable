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
    getMortalitySpecies(state) {
      const rowList = state.mortalityData.features.map(
        (i) => i.properties?.species
      );
      let unique = rowList.filter(
        (value, index, self) =>
          index ===
          self.findIndex(
            (t) => t.id === value.id
          )
      );
      return unique;
    },

    getMortalityItem(state) {
      return state.mortalityItem;
    },
  },
  actions: {
    async getMortalityData(
      params: { [key: string]: string | null },
      controller: AbortController
    ) {
      try {
        const data = await $http.$get("/api/v1/mortality/", {
          signal: controller.signal,
          params,
        });
        this.mortalityData = data;
        console.log('this.mortalityData', this.mortalityData)
      } catch (error) {
        console.error(error);
      }
    },
    setMortalityItem(data: Feature) {
      this.mortalityItem = data;
    },
    setMortalityData (data: FeatureCollection) {
      this.mortalityData = data
    },
  },
});

