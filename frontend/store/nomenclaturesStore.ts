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
 * armingItems: list of Items related to Type of Point Infrastructure (Pole/Pylones)
 * riskLevelItems: list of Items related to Risk Level assessment
 */
import { defineStore } from "pinia";
import * as errorCodes from "~/static/errorConfig.json";
import type { ErrorInfo } from "~/store/errorStore";

export const useNomenclaturesStore = defineStore("nomenclatures", {
  state: () => ({
    nomenclatureTypes: [] as NomenclatureType[],
  }),
  getters: {
    armingItems(state) {
      return state.nomenclatureTypes.find((elem: NomenclatureType) => elem.code === "ARMING")?.nomenclatures;
    },
    ownerItems(state) {
      return state.nomenclatureTypes.find((elem: NomenclatureType) => elem.code === "OWNER")?.nomenclatures;
    },
    riskLevelItems(state) {
      return state.nomenclatureTypes.find((elem: NomenclatureType) => elem.code === "RISK_LEV")?.nomenclatures;
    },
    deathCauseItems(state) {
      return state.nomenclatureTypes.find((elem: NomenclatureType) => elem.code === "CAUSE_OF_DEATH")?.nomenclatures;
    },
    equipmentTypeItems(state) {
      return state.nomenclatureTypes.find((elem: NomenclatureType) => elem.code === "EQMT_TYPE")?.nomenclatures;
    },
    conditionItems(state) {
      return state.nomenclatureTypes.find((elem: NomenclatureType) => elem.code === "IFR_COND")?.nomenclatures;
    },
    infrastructureType(state) {
      return state.nomenclatureTypes.find((elem: NomenclatureType) => elem.code === "IFR_TYPE")?.nomenclatures;
    },
    getInfrastructureTypeId() {
      return (geomType: string) => {
        console.log('geomType', geomType)
        const code = geomType.toLowerCase() === 'point' ? 'POLE' : 'LINE'
        return this.infrastructureType?.find((elem: NomenclatureItem) => elem.code === code)?.id
      }
    },
    getArmingItems() {
      return (geomType: string ,owner: string) => {
        console.log('geomType', geomType)
        const code = geomType.toLowerCase() === 'point' ? 'POLE' : 'LINE'
        const infraTypeId: number | undefined  = this.infrastructureType?.find((elem: NomenclatureItem) => elem.code === code)?.id
        return infraTypeId? this.armingItems?.filter(item => item.parents?.includes(infraTypeId)):[]
      }
    },
    getEquipmentItems() {
      return (geomType: string , owner: string) => {
        console.log('geomType', geomType)
        const code = geomType.toLowerCase() === 'point' ? 'POLE' : 'LINE'
        const infraTypeId: number | undefined  = this.infrastructureType?.find((elem: NomenclatureItem) => elem.code === code)?.id
        return infraTypeId? this.equipmentTypeItems?.filter(item => item.parents?.includes(infraTypeId)):[]
      }
    }
  },
  actions: {
    async loadNomenclatures() {
      try {
        const params = { with_nomenclatures: true };
        this.nomenclatureTypes = await $http.$get("/api/v1/nomenclatures/types", { params }); // get Types list
      } catch (err: unknown) {
        console.error(err)
      }
    }
  },
});

interface NomenclatureItem {
  code: string;
  id: number;
  label: string;
  mnemonic: string;
  type: number;
  parents?: number[];
}

interface NomenclatureType {
  id: number;
  code: string;
  mnemonic: string;
  label: string;
  nomenclatures: NomenclatureItem[];
}
