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
import type { ErrorInfo } from "~/store/errorStore";

export const useNomenclaturesStore = defineStore("nomenclatures", {
  state: () => ({
    nomenclatures: [] as NomenclatureType[],
    conditionItems: [] as NomenclatureItem[],
    ownerItems: [] as NomenclatureItem[],
    poleTypeItems: [] as NomenclatureItem[],
    riskLevelItems: [] as NomenclatureItem[],
    deathCauseItems: [] as NomenclatureItem[],
    operationTypeItems: [] as NomenclatureItem[],
  }),
  getters: {
    /**
     * Getter for infrastructure condition nomenclature items.
     *
     * @param {state} state of this store module
     * @return {JSON object} returns the list of nomenclature items for infrastucture conditions
     */
    getNomenclatureByType(state) {
      return (mnemonic: string) =>
        state.nomenclatures.find(
          (elem: NomenclatureItem) => elem.mnemonic === mnemonic
        )?.item_nomenclature;
    },
  },
  actions: {
    /**
     * Store method to gather nomenclatures data in store (nomenclaturesStore)
     * Create a dictionnary with all Types, and each Type contains an array of Items.
     *
     * @param {context} context object set as destructured form { commit }
     */

    async loadNomenclatures() {
      try {
        const types = await $http.$get("/api/v1/nomenclatures/types"); // get Types list
        // gather Infrastructure Condition Items from all Items
        this.nomenclatures=types

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

interface NomenclatureType {
  id: number;
  code: string;
  mnemonic: string;
  label: string;
  item_nomenclature: NomenclatureItem[];
}
