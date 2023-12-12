import { defineStore } from "pinia";
import {mapBounds} from "./coordinatesStore"

export const useSpeciesStore = defineStore("species", {
  state: () => ({ species: [] }),
  getters: {
    getSpecies(state) {
      return state.species;
    },
  },
  // mutations: {
  //   addSpecies(state, data) {
  //     state.species = data;
  //   },
  // },
  actions: {
    async loadSpecies({ commit }) {
      try {
        const data = await this.$axios.$get("species/");
        if (data === undefined) {
          throw new Error("conditions");
        }
        // commit("addSpecies", data);
        this.species = data;
      } catch (err) {
        console.error("ERROR", err);
        const error = {};
        if (err.toString().includes("404")) {
          error.code = errorCodes.nomenclature_not_found.code;
          error.msg = $nuxt.$t(
            `error.${errorCodes.nomenclature_not_found.msg}`
          );
          // if nuxt error message contains substring 'conditions'
        }
        commit("errorStore/setError", error, { root: true });
        // log out user as application may not be reliable as is
        $nuxt.$auth.logout();
      }
    },
  },
});
