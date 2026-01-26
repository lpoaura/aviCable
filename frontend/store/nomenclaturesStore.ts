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
 * networkTypeItems: list of Items related to Infrastructure Owners
 * armingItems: list of Items related to Type of Point Infrastructure (Pole/Pylones)
 * riskLevelItems: list of Items related to Risk Level assessment
 */
import { defineStore } from "pinia";

export const useNomenclaturesStore = defineStore("nomenclatures", {
  state: () => ({
    nomenclatureTypes: [] as NomenclatureType[],
  }),
  getters: {
    areas(state) {
      return state.nomenclatureTypes?.find((elem: NomenclatureType) => elem.mnemonic === "geographic_areas")?.nomenclatures;
    },
    armingItems(state) {
      return state.nomenclatureTypes?.find((elem: NomenclatureType) => elem.code === "ARMING")?.nomenclatures;
    },
    networkTypeItems(state) {
      return state.nomenclatureTypes?.find((elem: NomenclatureType) => elem.code === "NETW_TYP")?.nomenclatures;
    },
    riskLevelItems(state) {
      return state.nomenclatureTypes?.find((elem: NomenclatureType) => elem.code === "RISK_LEV")?.nomenclatures;
    },
    deathCauseItems(state) {
      return state.nomenclatureTypes?.find((elem: NomenclatureType) => elem.code === "CAUSE_OF_DEATH")?.nomenclatures;
    },
    equipmentTypeItems(state) {
      return state.nomenclatureTypes?.find((elem: NomenclatureType) => elem.code === "EQMT_TYPE")?.nomenclatures;
    },
    conditionItems(state) {
      return state.nomenclatureTypes?.find((elem: NomenclatureType) => elem.code === "IFR_COND")?.nomenclatures;
    },
    infrastructureType(state) {
      return state.nomenclatureTypes?.find((elem: NomenclatureType) => elem.code === "IFR_TYPE")?.nomenclatures;
    },
    getInfrastructureTypeId() {
      return (geomType: string) => {
        console.debug('geomType', geomType)
        const code = geomType.toLowerCase() === 'point' ? 'POLE' : 'LINE'
        return this.infrastructureType?.find((elem: NomenclatureItem) => elem.code === code)?.id
      }
    },
    getArmingItems() {
      return (geomType: string, network_type: number) => {
        console.debug('<getArmingItems> geomType', geomType, 'networkType',network_type)
        const code = geomType.toLowerCase() === 'point' ? 'POLE' : 'LINE'
        const infraTypeId: number | undefined = this.infrastructureType?.find((elem: NomenclatureItem) => elem.code === code)?.id
        console.debug('<getArmingItems> infraTypeId', infraTypeId)
        console.debug('<getArmingItems>',infraTypeId ? (this.armingItems?.filter(item => item.parents?.includes(infraTypeId)))?.filter(item => item.parents?.includes(network_type)) : [])
        return infraTypeId ? (this.armingItems?.filter(item => item.parents?.includes(infraTypeId)))?.filter(item => item.parents?.includes(network_type)) : []
      }
    },
    getEquipmentItems() {
      return (geomType: string) => {
        console.debug('geomType', geomType)
        const code = geomType.toLowerCase() === 'point' ? 'POLE' : 'LINE'
        const infraTypeId: number | undefined = this.infrastructureType?.find((elem: NomenclatureItem) => elem.code === code)?.id
        console.debug('<getEquipmentItems> infraTypeId', infraTypeId, this.equipmentTypeItems)
        return infraTypeId ? this.equipmentTypeItems?.filter(item => {
          return item.parents?.includes(infraTypeId)
        }) : []
      }
    }
  },
  actions: {
    async getNomenclatures() {
      try {
        const params = { with_nomenclatures: true };
        const config = useRuntimeConfig()
        try {
          const url = `${config.public.baseURL}/api/v1/nomenclatures/types`
          const nomenclatureTypes = await $fetch<NomenclatureType[]>(url, { params })
          if (nomenclatureTypes && Array.isArray(nomenclatureTypes)) {
            this.nomenclatureTypes = nomenclatureTypes as NomenclatureType[]; // Type assertion
          } else {
            console.error("Unexpected data format:", nomenclatureTypes, Array.isArray(nomenclatureTypes));
          }
        } catch (error) {
          console.error(error);
        }
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
