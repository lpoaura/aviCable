// import { defineStore } from "pinia";
// import { notificationStore } from ".";
//
// export const useSpeciesStore = defineStore("species", {
//   state: () => ({ species: [] }),
//   getters: {
//     getSpecies(state) {
//       return state.species;
//     },
//   },
//   // mutations: {
//   //   addSpecies(state, data) {
//   //     state.species = data;
//   //   },
//   // },
//   actions: {
//     async loadSpecies({ commit }) {
//       try {
//         const data = await this.$axios.$get("species/");
//         if (data === undefined) {
//           throw new Error("conditions");
//         }
//         // commit("addSpecies", data);
//         this.species = data;
//       } catch (err) {
//         console.error("ERROR", err);
//         notificationStore.setInfo({
//           type: 'error',
//           msg: err.toString()
//         })
//         // $nuxt.$auth.logout();
//       }
//     },
//   },
// });
