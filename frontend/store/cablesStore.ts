// Nuxt Store module: cablesStore for Cables module
import { defineStore } from 'pinia'
import type { CablesFeatureCollection, OperationFeatureCollection, Line, Point, CablesFeature, Equipment, NetworkFeatureCollection, Infrastructure } from '~/types/cables'
import type { FeatureCollection } from 'geojson'

export const useCablesStore = defineStore('cables', {
  state: () => ({
    infstrData: {} as CablesFeatureCollection, // Infrastructure data
    infstrDataLoadingStatus: false,
    // pointData: {}, // Pole and Pylon data
    // lineData: {}, // Cable lines data
    opData: {} as OperationFeatureCollection,
    pointOpData: [] as Line[],
    lineOpData: [] as Point[],
    formDate: new Date() as Date,
    formInfrastructureId: null as number | null,
    formInfrastructure: {} as CablesFeature,
    controller: null as AbortController | null,
    enedisInfrastructure: {} as NetworkFeatureCollection,
    rteInfrastructure: {} as FeatureCollection,
    formEquipments: [] as Equipment[],
    selectedEquipment: null as Equipment | null,
    equipmentToDelete: null as Equipment | null,
  }),
  getters: {
    getFormDate: (state) => state.formDate,
    infstrDatafeatures(state): CablesFeature[] {
      return state.infstrData.features
    },
    countInfstr(): number | undefined {
      return this.infstrDatafeatures?.length
    },
    countOperatedInfstr(): number | undefined {
      return this.infstrDatafeatures?.length
    },
    pointData(state) {
      const filteredFeatures = state.infstrData.features?.filter(
        elem => elem.resourcetype === 'Point'
      )
      return {
        type: "FeatureCollection",
        features: filteredFeatures || []
      }
    },
    operatedInfstr(state) {
      return {
        type: "FeatureCollection",
        features: state.opData?.features || []
      }
    },
    operatedPointData(state) {
      const filteredFeatures = state.opData.features?.filter(
        elem => elem.geometry.type === 'Point'
      )
      return {
        type: "FeatureCollection",
        features: filteredFeatures || []
      }
    },
    operatedLineStringData(state) {
      const filteredFeatures = state.opData.features?.filter(
        elem => elem.geometry.type === 'LineString'
      )
      return {
        type: "FeatureCollection",
        features: filteredFeatures || []
      }
    },
    lineStringData(state) {
      const filteredFeatures = state.infstrData.features?.filter(
        elem => elem.resourcetype === 'Line'
      )
      return {
        type: "FeatureCollection",
        features: filteredFeatures || []
      }
    },
  },
  actions: {
    setFormDate(date: Date) {
      console.debug("Store setFormDate", date)
      this.formDate = date;
    },
    async getInfstrData(params: Object) {
      if (this.controller === null) {
        this.controller = new AbortController();
      }
      const { signal } = this.controller;
      console.debug('<getInfstrData> this.controller', this.controller)
      try {
        this.infstrDataLoadingStatus = true
        console.debug("getInfstrData signal", signal)
        const data = await api.get<CablesFeatureCollection>(
          '/api/v1/cables/infrastructures/', { signal, params }
        )
        this.infstrData = data
        this.infstrDataLoadingStatus = false
      } catch (error) {
        if (error instanceof Error && error.name === 'AbortError') {
          console.debug('getInfstrData Requête annulée');
        } else {
          console.error(error)
        }
      } finally {
        // Reset loading status and controller
        this.infstrDataLoadingStatus = false;
        this.controller = null; // Reset the controller after the request
      }

    },
    async getOpData(params) {
      if (this.controller === null) {
        this.controller = new AbortController();
      }
      const { signal } = this.controller;
      try {
        const data = await api.get<OperationFeatureCollection>(
          '/api/v1/cables/operations/', { signal, params }
        )
        this.opData = data
      } catch (error) {
        if (error instanceof Error && error.name === 'AbortError') {
          console.debug('getOpData Requête annulée');
        } else {
          console.error(error)
        }
      } finally {
        // Reset loading status and controller
        this.controller = null; // Reset the controller after the request
      }

    },
    async getAllInfrastructureData(params) {
      if (this.controller === null) {
        this.controller = new AbortController();
      }
      const { signal } = this.controller;
      try {
        const [infstrData, opData] = await Promise.all([
          api.get<CablesFeatureCollection>(
            '/api/v1/cables/infrastructures', { signal, params }
          ),
          api.get<OperationFeatureCollection>(
            '/api/v1/cables/operations/', { signal, params }
          ),
        ]);
        this.opData = opData
        this.infstrData = infstrData
        this.infstrDataLoadingStatus = false
      } catch (error) {
        if (error instanceof Error && error.name === 'AbortError') {
          console.debug('getAllInfrastructureData Requête annulée');
        } else {
          console.error(error)
        }
      } finally {
        // Reset loading status and controller
        this.controller = null; // Reset the controller after the request
      }
    },
    async getEnedisInfrastructure(bbox: string) {
      console.debug('bbox', bbox)
      const params = {
        bbox: bbox,
        //bbox: `${bbox[1]},${bbox[0]},${bbox[3]},${bbox[2]}`,
        format: "geojson",
        size: "10000",
      }
      if (this.controller === null) {
        this.controller = new AbortController();
      }
      const { signal } = this.controller;
      console.debug('getEnedisInfrastructure', signal)
      console.debug('query params', { signal, params })
      try {
        const [{ data: reseauBt }, { data: reseauHta }, { data: poteaux }] = await Promise.all([
          useFetch<NetworkFeatureCollection>(
            'https://opendata.enedis.fr/data-fair/api/v1/datasets/reseau-bt/lines', { signal, params }
          ),
          // useFetch<NetworkFeatureCollection>(
          //   'https://opendata.enedis.fr/data-fair/api/v1/datasets/reseau-souterrain-bt/lines', { signal, params }
          // ),
          useFetch<NetworkFeatureCollection>(
            'https://opendata.enedis.fr/data-fair/api/v1/datasets/reseau-hta/lines', { signal, params }
          ),
          // useFetch<NetworkFeatureCollection>(
          //   'https://opendata.enedis.fr/data-fair/api/v1/datasets/reseau-souterrain-hta/lines', { signal, params }
          // ),
          useFetch<NetworkFeatureCollection>(
            'https://opendata.enedis.fr/data-fair/api/v1/datasets/position-geographique-des-poteaux-hta-et-bt/lines', { signal, params }
          )
        ]);
        if (reseauBt.value && reseauHta.value && poteaux.value) {
          reseauBt.value.features.forEach(v => {
            if (v.properties) {
              v.properties.type = 'Overhead'
              v.properties.category = 'bt'
            }
          })
          // reseauSoutBt.value.features.forEach(v => {
          //   if (v.properties) {
          //     v.properties.type = 'Underground'
          //     v.properties.category = 'bt'
          //   }
          // })
          reseauHta.value.features.forEach(v => {
            if (v.properties) {
              v.properties.type = 'Overhead'
              v.properties.category = 'hta'
            }
          })
          // reseauSoutHta.value.features.forEach(v => {
          //   if (v.properties) {
          //     v.properties.type = 'Underground'
          //     v.properties.category = 'hta'
          //   }
          // })
          poteaux.value.features.forEach(v => {
            if (v.properties) {
              v.properties.type = 'Overhead'
              v.properties.category = 'hta'
            }
          })
          this.enedisInfrastructure = {
            type: 'FeatureCollection',
            features: [...reseauBt.value.features, ...reseauHta.value.features, ...poteaux.value.features,]
          }
        }
      } catch (error) {
        if (error instanceof Error && error.name === 'AbortError') {
          console.debug('getEnedisInfrastruc        ture Requête annulée');
        } else {
          console.error(error)
        }
      } finally {
        // Reset loading status and controller
        this.controller = null; // Reset the controller after the request
      }
    },
    async getRteInfrastructure(bbox: string) {
      const paramsLines = {
        where: `in_bbox(geo_shape,${bbox})`,
        limit: "10000",
        lang: "fr",
        timezone: "Europe/Paris",
        use_labels: "false",
        epsg: "4326"
      }
      const paramsPylones = { ...paramsLines }
      paramsPylones.where = `in_bbox(geo_point_pylone,${bbox})`
      if (this.controller === null) {
        this.controller = new AbortController();
      }
      const { signal } = this.controller;
      try {
        const [{ data: Lines }, { data: Pylones }] = await Promise.all([
          useFetch<FeatureCollection>(
            'https://odre.opendatasoft.com/api/explore/v2.1/catalog/datasets/lignes-aeriennes-rte-nv/exports/geojson', { signal, params: paramsLines }
          ),
          useFetch<FeatureCollection>(
            'https://odre.opendatasoft.com/api/explore/v2.1/catalog/datasets/pylones-rte/exports/geojson', { signal, params: paramsPylones }
          ),
        ]);
        if (Lines.value && Pylones.value) {
          this.rteInfrastructure = {
            type: 'FeatureCollection',
            features: [...Lines.value.features, ...Pylones.value.features]
          }
        }

      } catch (error) {
        if (error instanceof Error && error.name === 'AbortError') {
          console.debug('getRteInfrastructure Requête annulée');
        } else {
          console.error(error)
        }
      } finally {
        // Reset loading status and controller
        this.controller = null; // Reset the controller after the request
      }
    },
    cancelRequest() {
      console.debug('cancelRequest abort request - 1', this.controller)
      this.controller?.abort()
      console.debug('cancelRequest abort request - 2', this.controller)
      this.controller = null;
      console.debug('cancelRequest abort request - 3', this.controller)
    },
    setFormInfrastructureId(id: number) {
      this.formInfrastructureId = id
    },
    setFormInfrastructure(infrastructure: CablesFeature) {
      this.formInfrastructure = infrastructure
    },
    addSelectedToEquipments() {
      console.debug('addSelectedToMedias')
      if (this.selectedEquipment?.id) {
        this.formEquipments[this.formEquipments.findIndex(item => item.id === this.selectedEquipment?.id)] = this.selectedEquipment
      } else {
        !!this.selectedEquipment && this.formEquipments.push(this.selectedEquipment)
      }
      this.selectedEquipment = {} as Equipment
    },
    // addSelectedToEquipments() {
    //   if (this.selectedEquipment?.id) {
    //     const index = this.formEquipments.findIndex(item => item.id === this.selectedEquipment.id);
    //     if (index !== -1) {
    //       this.formEquipments[index] = this.selectedEquipment;
    //     }
    //   } else if (this.selectedEquipment) {
    //     this.formEquipments.push(this.selectedEquipment);
    //   }

    //   this.selectedEquipment = {} as Equipment;
    // },
    resetFormEquipments() {
      this.formEquipments = [] as Equipment[]
    },
    // setEquipments(data: Equipment[]) {
    //   this.formEquipments = data
    // }
    async deleteEquipment(index: number) {
      try {
        this.equipmentToDelete = this.formEquipments[index]
        const equipment = { ...this.equipmentToDelete }
        console.debug('this.mediaToDelete test', (index !== null), this.equipmentToDelete, this.equipmentToDelete.id)
        // if (this.equipmentToDelete && this.equipmentToDelete.id) {
        //   const { data: _resp } = await api.get<Media>(`/api/v1/media/${this.mediaToDelete.id}`, { method: 'DELETE' });
        // }
        this.formEquipments.splice(index, 1)
        notificationStore.setInfo({
          type: 'success',
          msg: `Equipment ${equipment.type?.code} - ${equipment.count} successfully deleted`
        })
      } catch (error) {
        notificationStore.setInfo({
          type: 'error',
          msg: `Delete Equipment failed : ${error}`
        })
      }
    }

  }
})
