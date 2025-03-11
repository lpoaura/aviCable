/**
 * mapLayerStore to handle map layers loading
 */

import { defineStore } from "pinia";
import type { FeatureCollection, Feature } from "geojson";
import type { MortalityStoreState, Species, MortalityData } from "~/types/mortality";


export const useMortalityStore = defineStore("mortality", {
  state: (): MortalityStoreState => ({
    mortalityData: {} as FeatureCollection,
    mortalityItem: {} as Feature,
    error: null,
    controller: null,
  }),
  getters: {
    // // get FeatureCollection data
    // infstrData(state) {
    //   return state.infstrData
    // },
    // get FeatureCollection array containing data (Json Object)
    getMortalityFeatures(state): Feature[] {
      return state.mortalityData?.features;
    },
    getMortalitySpecies(state): Species[] {
      const rowList = state.mortalityData?.features.map(
        (i) => i.properties?.species
      );
      const unique = rowList.filter(
        (value, index, self) =>
          index === self.findIndex((t) => t.id === value.id)
      );
      return unique;
    },
    getMortalityItem(state): Feature {
      return state.mortalityItem;
    },
    getterMortalityData(state): FeatureCollection {
      return state.mortalityData;
    },
    countMortality(state) {
      return state.mortalityData?.features?.length
    },
  },
  actions: {
    async getMortalityData(params: { [key: string]: string | null }) {
      this.controller = new AbortController();
      const { signal } = this.controller;
      console.debug("getMortalityData", this.controller, signal);
      try {
        const { data: data } = await useApi<FeatureCollection>("/api/v1/mortality/", { signal, params });
        if (data.value) { this.mortalityData = data.value };
      } catch (error: any) {
        if (error instanceof Error && error.name === "AbortError") {
          console.debug("Requête annulée");
        } else {
          console.error(error);
        }
      }
    },
    cancelRequest() {
      console.log('mortality abort request')
      this.controller?.abort()
      this.controller = null;
    },
    setMortalityItem(data: Feature) {
      this.mortalityItem = data;
    },
    setMortalityData(data: FeatureCollection) {
      this.mortalityData = data;
    },
  },
});
