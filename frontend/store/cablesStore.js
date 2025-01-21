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
      if (this.controller === null) {
        this.controller = new AbortController();
      }
      const { signal } = this.controller;
      console.log('<getInfstrData> this.controller', this.controller)
      try {
        this.infstrDataLoadingStatus = true
        console.debug("getInfstrData signal", signal)
        await useApi(
          '/api/v1/cables/infrastructures', {signal, params}
        ).then(data => {
          this.infstrData = data.value
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
      if (this.controller === null) {
        this.controller = new AbortController();
      }
      const { signal } = this.controller;
      console.debug('getOpData', signal)
      try {
        console.debug("getOpData signal", signal)
        await useApi(
          '/api/v1/cables/operations/', {signal, params}
        ).then(data => {
          this.opData = data.value
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
      if (this.controller === null) {
        this.controller = new AbortController();
      }
      const { signal } = this.controller;
      console.debug('getAllInfrastructureData', {signal: this.controller.signal , params}, {signal , params})
      try {
        console.debug("getAllInfrastructureData signal", signal)
        const [ {data: infstrData}, {data: opData} ] = await Promise.all([
          useApi(
            '/api/v1/cables/infrastructures', {signal, params}
          ),
          useApi(
            '/api/v1/cables/operations/', {signal, params}
          ),
        ]);
        this.opData = opData.value
        this.infstrData = infstrData.value
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
      if (this.controller === null) {
        this.controller = new AbortController();
      }
      const { signal } = this.controller;
      console.debug('getEnedisInfrastructure', signal)
      console.log('query params', {signal, params})
      try{
        const [ {data: reseauBt }, {data: reseauHta}, {data: poteaux}] = await Promise.all([
          useApi(
            'https://data.enedis.fr/api/explore/v2.1/catalog/datasets/reseau-bt/exports/geojson', {signal, params}
          ),
          useApi(
            'https://data.enedis.fr/api/explore/v2.1/catalog/datasets/reseau-hta/exports/geojson', {signal, params}
          ),
          useApi(
            'https://data.enedis.fr/api/explore/v2.1/catalog/datasets/position-geographique-des-poteaux-hta-et-bt/exports/geojson', {signal, params}
          )
        ]);
        this.enedisInfrastructure = {
          type: 'FeatureCollection',
          features : [...reseauBt.value.features,...reseauHta.value.features,...poteaux.value.features,]
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
      if (this.controller === null) {
        this.controller = new AbortController();
      }
      const { signal } = this.controller;
      console.debug('getRteInfrastructure signal', signal)
      console.log('query params', {signal, params: paramsPylones})
      try{
        const [ {data: Lines}, {data: Pylones}] = await Promise.all([
          useApi(
            'https://odre.opendatasoft.com/api/explore/v2.1/catalog/datasets/lignes-aeriennes-rte-nv/exports/geojson', {signal, params: paramsLines}
          ),
          useApi(
            'https://odre.opendatasoft.com/api/explore/v2.1/catalog/datasets/pylones-rte/exports/geojson', {signal, params: paramsPylones}
          ),
        ]);
        this.rteInfrastructure = {
          type: 'FeatureCollection',
          features : [...Lines.value.features,...Pylones.value.features]
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
      console.log('cancelRequest abort request - 1', this.controller)
      this.controller?.abort()
      console.log('cancelRequest abort request - 2', this.controller)
      this.controller = null;
      console.log('cancelRequest abort request - 3', this.controller)
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
