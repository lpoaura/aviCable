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
    enedisInfrastructure: null,
    rteInfrastructure: null,
  }),
  getters: {
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
      const filteredFeatures=state.infstrData.features?.filter(
        elem => elem.resourcetype === 'Point'
      )
      return {
        type: "FeatureCollection",
        features: filteredFeatures || []
      }
    },
    operatedInfstr (state) {
      return {
        type: "FeatureCollection",
        features: state.opData?.features || []
      }
    },
    operatedPointData (state) {
      const filteredFeatures=state.opData.features?.filter(
        elem => elem.geometry.type === 'Point'
      )
      return {
        type: "FeatureCollection",
        features: filteredFeatures || []
      }
    },
    operatedLineStringData (state) {
      const filteredFeatures=state.opData.features?.filter(
        elem => elem.geometry.type === 'LineString'
      )
      return {
        type: "FeatureCollection",
        features: filteredFeatures || []
      }
    },
    lineStringData (state) {
      const filteredFeatures=state.infstrData.features?.filter(
        elem => elem.resourcetype === 'Line'
      )
      return {
        type: "FeatureCollection",
        features: filteredFeatures || []
      }
    },
  },
  actions: {
    async getInfstrData (params) {
      this.controller = new AbortController();
      const { signal } = this.controller;
      console.debug('getInfstrData', signal)
      try {
        this.infstrDataLoadingStatus = true
        console.debug("getInfstrData signal", signal)
        await $http.$get(
          '/api/v1/cables/infrastructures', {signal, params}
        ).then(data => {
          this.infstrData = data
          this.infstrDataLoadingStatus = false
        })
      } catch (err) {
        if (err.name === 'AbortError') {
          console.debug('getInfstrData Requête annulée');
        } else {
          console.error(err)
        }
      }  finally {
        // Reset loading status and controller
        this.infstrDataLoadingStatus = false;
        this.controller = null; // Reset the controller after the request
      }

    },
    async getOpData (params) {
      this.controller = new AbortController();
      const { signal } = this.controller;
      console.debug('getOpData', signal)
      try {
        console.debug("getOpData signal", signal)
        await $http.$get(
          '/api/v1/cables/operations/', {signal, params}
        ).then(data => {
          this.opData = data
        })
      } catch (err) {
        if (err.name === 'AbortError') {
          console.debug('getOpData Requête annulée');
        } else {
          console.error(err)
        }
      }  finally {
        // Reset loading status and controller
        this.controller = null; // Reset the controller after the request
      }

    },
    async getAllInfrastructureData(params) {
      this.controller = new AbortController();
      const { signal } = this.controller;
      console.debug('getAllInfrastructureData', signal)
      try {
        console.debug("getAllInfrastructureData signal", signal)
        const [ infstrData, opData] = await Promise.all([
          $http.$get(
            '/api/v1/cables/infrastructures', {signal, params}
          ),
          $http.$get(
            '/api/v1/cables/operations/', {signal, params}
          ),
        ]);
        this.opData = opData
        this.infstrData = infstrData
        this.infstrDataLoadingStatus = false
      } catch (err) {
        if (err.name === 'AbortError') {
          console.debug('getAllInfrastructureData Requête annulée');
        } else {
          console.error(err)
        }
      }  finally {
        // Reset loading status and controller
        this.controller = null; // Reset the controller after the request
      }
    },
    async getEnedisInfrastructure (bbox) {
      const params =         {
          where: `in_bbox(geo_shape,${bbox})` ,
          limit: "10000",
          lang: "fr",
          timezone: "Europe/Paris",
          use_labels: "false",
          epsg: "4326"
      }
      this.controller = new AbortController();
      const { signal } = this.controller;
      console.debug('getEnedisInfrastructure', signal)
      try{
        const [ reseauBt, reseauHta, poteaux] = await Promise.all([
          $http.$get(
            'https://data.enedis.fr/api/explore/v2.1/catalog/datasets/reseau-bt/exports/geojson', {signal, params}
          ),
          $http.$get(
            'https://data.enedis.fr/api/explore/v2.1/catalog/datasets/reseau-hta/exports/geojson', {signal, params}
          ),
          $http.$get(
            'https://data.enedis.fr/api/explore/v2.1/catalog/datasets/position-geographique-des-poteaux-hta-et-bt/exports/geojson', {signal, params}
          )
        ]);
        this.enedisInfrastructure = {
          type: 'FeatureCollection',
          features : [...reseauBt.features,...reseauHta.features,...poteaux.features,]
        }

    } catch (err) {
      if (err.name === 'AbortError') {
        console.debug('getEnedisInfrastructure Requête annulée');
      } else {
        console.error(err)
      }
    }  finally {
      // Reset loading status and controller
      this.controller = null; // Reset the controller after the request
    }
    },
    async getRteInfrastructure (bbox) {
      const paramsLines =         {
          where: `in_bbox(geo_shape,${bbox})` ,
          limit: "10000",
          lang: "fr",
          timezone: "Europe/Paris",
          use_labels: "false",
          epsg: "4326"
      }
      const paramsPylones = {...paramsLines}
      paramsPylones.where =  `in_bbox(geo_point_pylone,${bbox})`
      this.controller = new AbortController();
      const { signal } = this.controller;
      console.debug('getRteInfrastructure', signal)
      try{
        const [ Lines, Pylones] = await Promise.all([
          $http.$get(
            'https://odre.opendatasoft.com/api/explore/v2.1/catalog/datasets/lignes-aeriennes-rte-nv/exports/geojson', {signal, params: paramsLines}
          ),
          $http.$get(
            'https://odre.opendatasoft.com/api/explore/v2.1/catalog/datasets/pylones-rte/exports/geojson', {signal, params: paramsPylones}
          ),
        ]);
        console.log('Pylones', Pylones)
        this.rteInfrastructure = {
          type: 'FeatureCollection',
          features : [...Lines.features,...Pylones.features]
        }

    } catch (err) {
      if (err.name === 'AbortError') {
        console.debug('getRteInfrastructure Requête annulée');
      } else {
        console.error(err)
      }
    }  finally {
      // Reset loading status and controller
      this.controller = null; // Reset the controller after the request
    }
    },
    cancelRequest() {
      console.debug('cancelRequest aborting getInfstrData check',this.controller)
      if (this.controller) {
        console.debug('cancelRequest aborting getInfstrData',this.controller)
        this.controller.abort();
        this.controller = null; // Reset the controller after aborting
        console.debug('cancelRequest aborted getInfstrData', this.controller)
      } else {
        console.debug('cancelRequest No request to abort');
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
      this.infstrData = data
    },
    addOperation (data) {
      this.opData = data.all
      this.pointOpData = data.point
      this.lineOpData = data.line
    }
  }
})
