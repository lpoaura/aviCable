/** Nuxt Store module: saStore for Sensible Area module */

import { defineStore } from 'pinia'

export const useSensitiveAreasStore = defineStore('sensitiveAreas', {
  state: () => ({ SAData: {} }),
  getters: {
    saData (state) {
      return state.SAData
    },
    saDataFeatures (state) {
      return state.SAData.features
    }
  }
})

// export const state = () => ({
//   /** Sensible Area data get from fetch request as geoJson object */
//   SAData: {},
// });

// export const mutations = {
//   /**
//    * Mutation: apply value change to state of current store module
//    *
//    * @param {state} state of this store module
//    * @param {geoJson object} contains Sensitive Area data get from fetch request
//    */
//   add(state, data) {
//     state.SAData = data;
//   },
// };

// export const getters = {
//   /**
//    * Getter for Sensitive Area data as geoJson object
//    *
//    * @param {state} context of this store module
//    * @return {geoJson object} contains Sensitive Area data
//    */
//   SAData(state) {
//     return state.SAData;
//   },
//   /**
//    * Getter for Sensitive Area data as FeatureCollection object
//    *
//    * @param {state} context of this store module
//    * @return {FeatureCollection} array of Features contained by geoJson data for Sensitive Area
//    */
//   SADataFeatures(state) {
//     return state.SAData.features;
//   },
// };
