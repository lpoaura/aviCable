/**
 * mapLayerStore to handle map layers loading
 */

import { defineStore } from "pinia";
import type { FeatureCollection, Feature } from "geojson";

import { useCoordinatesStore } from "./coordinatesStore";

interface MortalityStoreState {
  mortalityData: FeatureCollection; // Replace 'any' with a more specific type if possible
  mortalityItem: Feature;
  error: Error | null;
  controller: AbortController | null;
}

interface MortalityData {
  properties: {
    id: number;
    vernacular_name: string;
    scientific_name: string;
    death_cause?: string;
    default: boolean | undefined;
  };
}

interface Species {
  id: number;
  vernacular_name: string;
  scientific_name: string;
}

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
      return state.mortalityData.features;
    },
    getMortalitySpecies(state): Species[] {
      const rowList = state.mortalityData.features.map(
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
    countMortality(state) {
      return state.mortalityData.features?.length
    },
  },
  actions: {
    async getMortalityData(params: { [key: string]: string | null }) {
      this.controller = new AbortController();
      const { signal } = this.controller;
      console.debug("getMortalityData",this.controller, signal);
      try {
        const data = await $http.$get("/api/v1/mortality/", { signal, params });
        this.mortalityData = data;
      } catch (err: unknown) {
        if (err.name === "AbortError") {
          console.debug("Requête annulée");
        } else {
          console.error(err);
        }
      }
    },
    cancelRequest() {
      console.debug('aborting getMortalityData check',this.controller)
      if (this.controller) {
        console.debug('aborting getMortalityData',this.controller)
        this.controller.abort();
        this.controller = null; // Reset the controller after aborting
        console.debug('aborted getMortalityData', this.controller)
      }
    },
    setMortalityItem(data: Feature) {
      this.mortalityItem = data;
    },
    setMortalityData(data: FeatureCollection) {
      this.mortalityData = data;
    },
  },
});
