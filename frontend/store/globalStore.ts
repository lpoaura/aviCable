/**
 * mapLayerStore to handle map layers loading
 */

import { defineStore } from "pinia";

interface GlobalStoreState {
  drawer: boolean; // Replace 'any' with a more specific type if possible
  userAvatar: number;
}

export const useGlobalStore = defineStore("global", {
  state: (): GlobalStoreState => ({
    drawer: false,
    userAvatar: 7
  }),
  getters: {
    getUserAvatar(state) {
      state.userAvatar = Math.floor(Math.random() * (9 - 2 + 1) + 2)
    }
  },
  actions: {
    setUserAvatar() {
      this.userAvatar = Math.floor(Math.random() * (9 - 2 + 1) + 2)
    }
  }
});
