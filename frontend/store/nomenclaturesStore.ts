/** Nuxt Store module: NomenclatureStore for Nomenclature module
 *
 * Nomenclature define Source, Type and Item data. It works as a data dictionnary for the
 * application. Each Type is associated to a Source and each Item is associated to a Type.
 * Lot of fields in the DataBase Model from backend are associated to a Type. That means that
 * acceptable values for these fieds are all Items related to this field.
 * This allow standardisation and securisation of data recorded in DB, and in same time assuring
 * flexibility as the application remain configurable by updation Source/Type/Item in DB.
 *
 * conditionItems: list of Items related to Infrastructure Condition
 * ownerItems: list of Items related to Infrastructure Owners
 * poleTypeItems: list of Items related to Type of Point Infrastructure (Pole/Pylones)
 * riskLevelItems: list of Items related to Risk Level assessment
 */
import { defineStore } from "pinia";
import * as errorCodes from "~/static/errorConfig.json";
import { ErrorInfo } from "./errorStore";

export const useNomenclaturesStore = defineStore("nomenclatures", {
  state: () => ({
    conditionItems: [] as NomenclatureItem[],
    ownerItems: [] as NomenclatureItem[],
    poleTypeItems: [] as NomenclatureItem[],
    riskLevelItems: [] as NomenclatureItem[],
    deathCauseItems: [] as NomenclatureItem[],
  }),
  getters: {
    /**
     * Getter for infrastructure condition nomenclature items.
     *
     * @param {state} state of this store module
     * @return {JSON object} returns the list of nomenclature items for infrastucture conditions
     */
    getConditions(state) {
      return state.conditionItems;
    },
    /**
     * Getter for owner nomenclature items.
     *
     * @param {state} state of this store module
     * @return {JSON object} returns the list of nomenclature items for owners
     */
    getOwners(state) {
      return state.ownerItems;
    },
    /**
     * Getter for pole type nomenclature items.
     *
     * @param {state} state of this store module
     * @return {JSON object} returns the list of nomenclature items for pole types
     */
    getPoleTypes(state) {
      return state.poleTypeItems;
    },
    /**
     * Getter for risk level nomenclature items.
     *
     * @param {state} state of this store module
     * @return {JSON object} returns the list of nomenclature items for risk levels
     */
    getRiskLevels(state) {
      return state.riskLevelItems;
    },
    /**
     * Getter for death cause nomenclature items.
     *
     * @param {state} state of this store module
     * @return {JSON object} returns the list of nomenclature items for risk levels
     */
    getDeathCause(state) {
      return state.deathCauseItems;
    },
  },
  // mutations: {
  //   addSpecies(state, data) {
  //     state.species = data;
  //   },
  // },
  actions: {
    /**
     * Store method to gather nomenclatures data in store (nomenclaturesStore)
     * Create a dictionnary with all Types, and each Type contains an array of Items.
     *
     * @param {context} context object set as destructured form { commit }
     */
    async loadNomenclatures() {
      try {
        const types = await $http.$get("/api/v1/nomenclature/types/"); // get Types list
        // gather Infrastructure Condition Items from all Items
        const conditions = types.find(
          (elem: NomenclatureItem) => elem.mnemonic === "infrastr_condition"
        );
        // If no Items is gathered, an Error is thrown
        if (conditions === undefined) {
          throw new Error("conditions");
        }
        // set "conds" to state value "conditionItems"
        this.conditionItems = conditions.item_nomenclature;
        // gather Owner Items from all Items
        const owners = types.find(
          (elem: NomenclatureItem) => elem.mnemonic === "owner"
        );
        // If no Items is gathered, an Error is thrown
        if (owners === undefined) {
          throw new Error("owners");
        }
        // set "owners" to state value "ownerItems"
        this.ownerItems = owners.item_nomenclature;
        // gather Pole type Items from all Items
        const poleTypes = types.find(
          (elem: NomenclatureItem) => elem.mnemonic === "pole_type"
        );
        // If no Items is gathered, an Error is thrown
        if (poleTypes === undefined) {
          throw new Error("poleTypes");
        }
        // set "poletypes" to state value "poletypeItems"
        this.poleTypeItems = poleTypes.item_nomenclature;
        // // gather Risk Level Items from all Items
        const riskLevels = types.find(
          (elem: NomenclatureItem) => elem.mnemonic === "risk_level"
        );
        // If no Items is gathered, an Error is thrown
        if (riskLevels === undefined) {
          throw new Error("riskLevels");
        }
        // set "riskLevels" to state value "riskLevelItems"
        this.riskLevelItems = riskLevels.item_nomenclature;
        console.log("this.riskLevelItems", this.riskLevelItems);

        // // gather Death cause Items from all Items
        const deathCause = types.find(
          (elem: NomenclatureItem) => elem.mnemonic === "cause_of_death"
        );
        // If no Items is gathered, an Error is thrown
        if (deathCause === undefined) {
          throw new Error("deathCause");
        }
        // set "riskLevels" to state value "riskLevelItems"
        this.deathCauseItems = deathCause.item_nomenclature;

        // error handling
      } catch (err: unknown) {
        const error: ErrorInfo = {} as ErrorInfo;
        // if nuxt error message contains substring '404'
        if (err.toString().includes("404")) {
          error.code = errorCodes.nomenclature_not_found.code;
          error.msg = useNuxtApp().$i18n.t(
            `error.${errorCodes.nomenclature_not_found.msg}`
          );
          // if nuxt error message contains substring 'conditions'
        } else if (err.toString().includes("conditions")) {
          error.code = errorCodes.get_infrstr_conditions.code;
          error.msg = useNuxtApp().$i18n.t(
            `error.${errorCodes.get_infrstr_conditions.msg}`
          );
          // if nuxt error message contains substring 'owners'
        } else if (err.toString().includes("owners")) {
          error.code = errorCodes.get_infrstr_owners.code;
          error.msg = useNuxtApp().$i18n.t(
            `error.${errorCodes.get_infrstr_owners.msg}`
          );
          // if nuxt error message contains substring 'poleTypes'
        } else if (err.toString().includes("poleTypes")) {
          error.code = errorCodes.get_infrstr_poletypes.code;
          error.msg = useNuxtApp().$i18n.t(
            `error.${errorCodes.get_infrstr_poletypes.msg}`
          );
          // if nuxt error message contains substring 'riskLevels'
        } else if (err.toString().includes("riskLevels")) {
          error.code = errorCodes.get_infrstr_risklevels.code;
          error.msg = useNuxtApp().$i18n.t(
            `error.${errorCodes.get_infrstr_risklevels.msg}`
          );
          // Default error if not capture above
        } else {
          error.code = errorCodes.loading_whole_nomenclatures.code;
          error.msg = useNuxtApp().$i18n.t(
            `error.${errorCodes.loading_whole_nomenclatures.msg}`
          );
        }
        // set error message to errorStore and triggers message display through "err" watcher in
        // error-snackbar component

        // commit('errorStore/setError', error, { root: true })
        // log out user as application may not be reliable as is
        // $nuxt.$auth.logout();
      }
    },
  },
});

interface NomenclatureItem {
  code: string;
  id: number;
  label: string;
  mnemonic: string;
  type: number;
}
