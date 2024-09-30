// Nuxt Store module: cablesStore for Cables module
import { defineStore } from 'pinia'

export const useCablesStore = defineStore('cables', {
  state: () => ({
    infstrData: {}, // Infrastructure data
    infstrDataLoadingStatus: false,
    // pointData: {}, // Pole and Pylon data
    // lineData: {}, // Cable lines data
    opData: [],
    pointOpData: [],
    lineOpData: [],
    formSupportId: null,
    formInfrastructureId: null,
    formInfrastructure: null,
    controller: null,
  }),
  getters: {
    // // get FeatureCollection data
    // infstrData(state) {
    //   return state.infstrData
    // },
    // get FeatureCollection array containing data (Json Object)
    infstrDatafeatures (state) {
      return state.infstrData.features
    },
    countInfstr(state) {
      return state.infstrDatafeatures?.length
    },
    countOperatedInfstr(state) {
      return state.infstrDatafeatures?.length
    },
    pointData (state) {
      return state.infstrData.features?.filter(
        elem => elem.resourcetype === 'Point'
      )
    },
    operatedInfstr (state) {
      return state.infstrData.features?.filter(
        elem => elem.properties.operations.length > 0
      )
    },
    operatedPointData (state) {
      return state.infstrData.features?.filter(
        elem => elem.resourcetype === 'Point' && elem.properties.operations.length > 0
      )
    },
    operatedLineStringData (state) {
      return state.infstrData.features?.filter(
        elem => elem.resourcetype === 'Line' && elem.properties.operations.length > 0
      )
    },
    lineStringData (state) {
      return state.infstrData.features?.filter(
        elem => elem.resourcetype === 'Line'
      )
    },
  },
  actions: {
    async getInfstrData (params, _) {
      this.controller = new AbortController();
      const { signal } = this.controller;
      console.log('getInfstrData', signal)
      try {
        this.infstrDataLoadingStatus = true
        console.log("getInfstrData signal", signal)
        await $http.$get(
          '/api/v1/cables/infrastructures', {signal, params}
        ).then(data => {
          this.infstrData = data
          this.infstrDataLoadingStatus = false
        })
      } catch (err) {
        if (err.name === 'AbortError') {
          console.log('Requête annulée');
        } else {
          console.error(err)
        }
      }  finally {
        // Reset loading status and controller
        this.infstrDataLoadingStatus = false;
        this.controller = null; // Reset the controller after the request
      }

    },
    cancelRequest() {
      console.log('aborting getInfstrData check',this.controller)
      if (this.controller) {
        console.log('aborting getInfstrData',this.controller)
        this.controller.abort();
        this.controller = null; // Reset the controller after aborting
        console.log('aborted getInfstrData', this.controller)
      } else {
        console.log('getInfstrData No request to abort');
      }
    },
    setFormSupportId(supportId) {
      this.formSupportId = supportId
    },
    setFormInfrastructureId(id) {
      this.formInfrastructureId = id
    },
    setFormInfrastructure(infrastructure) {
      this.formInfrastructure = infrastructure
    },
    setInfstrDataLoadingStatus(status) {
      this.infstrDataLoadingStatus = status
    },
    setInfstrData (data) {
      console.log('STORE setInfstrData', data)
      this.infstrData = data
    },
    addOperation (data) {
      this.opData = data.all
      this.pointOpData = data.point
      this.lineOpData = data.line
    }
  }
})
