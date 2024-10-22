/**
 * mapLayerStore to handle map layers loading
 */

import { defineStore } from "pinia";

interface GlobalStoreState {
  drawer: boolean; // Replace 'any' with a more specific type if possible
}


export const useGlobalStore = defineStore("global", {
  state: (): GlobalStoreState => ({
    drawer: false,
  }),
});
