// Nuxt Store module: cablesStore for Cables module
import { defineStore } from 'pinia'

export const useCablesStore = defineStore('cables', {
  state: () => ({
    infstrData: {}, // Infrastructure data
    infrstrDataLoadingStatus: false,
    // pointData: {}, // Pole and Pylon data
    // lineData: {}, // Cable lines data
    opData: [],
    pointOpData: [],
    lineOpData: []
  }),
  getters: {
    getInfrstrDataLoadingStatus(state) {
      return state.infrstrDataLoadingStatus 
    },
    // // get FeatureCollection data
    // infstrData(state) {
    //   return state.infstrData
    // },
    // get FeatureCollection array containing data (Json Object)
    getInfstrDatafeatures (state) {
      return state.infstrData.features
    },
    // pointData(state) {
    //   return state.pointData
    // },
    getPointDataFeatures (state) {
      return state.infstrData.features?.filter(
        elem => elem.resourcetype === 'Point'
      )
    },
    getOperatedPointDataFeatures (state) {
      return state.infstrData.features?.filter(
        elem => elem.resourcetype === 'Point' && elem.properties.operations.length > 0
      )
    },
    // lineData(state) {
    //   return state.lineData
    // },
    getLineDataFeatures (state) {
      return state.infstrData.features?.filter(
        elem => elem.resourcetype === 'Line'
      )
    },
    getOperatedLineDataFeatures (state) {
      return state.infstrData.features?.filter(
        elem => elem.resourcetype === 'Line' && elem.properties.operations.length > 0
      )
    },
    getOpData (state) {
      return state.opData
    },
    getPointOpData (state) {
      return state.pointOpData
    },
    getLineOpData (state) {
      return state.lineOpData
    }
  },
  actions: {
    async getInfrstrData (params, controller) {
      try {
        this.setInfrstrDataLoadingStatus(true)
        await $http.$get(
          '/api/v1/cables/infrastructures', {signal: controller.signal, params}
        ).then(data => {
          this.infstrData = data
          console.log('this.infstrData', this.infstrData)
          this.setInfrstrDataLoadingStatus(false)
        })
      } catch (error) {
        console.log(error)
      }
      this.setInfrstrDataLoadingStatus(false)
    },
    setInfrstrDataLoadingStatus(status) {
      this.infrstrDataLoadingStatus = status
    },
    setInfrstrData (data) {
      console.log('STORE setInfrstrData', data)
      this.infstrData = data
    },
    addOperation (data) {
      this.opData = data.all
      this.pointOpData = data.point
      this.lineOpData = data.line
    }
  }
})
