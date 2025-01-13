<template>
  <l-map id="map" ref="map" class="d-flex" :zoom="zoom" :center="center" @ready="hookUpDraw" @zoom="getBbox"
    @moveend="getBbox">
    <template v-if="mapReady">
      <l-tile-layer v-for="baseLayer in baseLayers" :key="baseLayer.id" :name="baseLayer.name" :url="baseLayer.url"
        :visible="baseLayer.default" :attribution="baseLayer.attribution" :layer-type="baseLayer.layer_type" />
      <template v-f="otherNetworksLayersReady = true">
        <l-geo-json v-for="(layer, index) in validInfrastructuresLayers" :key='index' :geojson="layer.data"
          :options="layer.options(layer.data)" :options-style="layer.optionsStyle" :name="layer.name"
          layer-type="overlay" @ready="infrastructureLayersReady = true" />
      </template>
      <template v-if="infrastructureLayersReady">
        <l-geo-json v-for="(layer, index) in validOperatedInfrastructuresLayers" :key='index' :geojson="layer.data"
          :options="layer.options(layer.data)" :options-style="layer.optionsStyle" :name="layer.name"
          layer-type="overlay" />
      </template>
      <l-geo-json v-for="(layer, index) in validOtherNetworksLayers" :key='index' :geojson="layer.data" :ref="layer.ref"
        :options="layer.options(layer.data)" :options-style="layer.optionsStyle" :name="layer.name" layer-type='overlay'
        @ready="otherNetworksLayersReady = true" :visible="layer.visible" />
      <l-geo-json v-if="isValidFeatureCollection(mortalityData)" name="Mortalité" layer-type="overlay"
        :geojson="mortalityData" :options="mortalityGeoJsonOptions()" />
      <l-geo-json v-if="bufferedSelectedInfrastructure" :geojson="bufferedSelectedInfrastructure"
        :options-style="bufferedSelectedInfrastructureGeoJsonOptionsStyle" />
      <l-geo-json v-if="bufferedMortalityInfrastructure" :geojson="bufferedMortalityInfrastructure"
        :options-style="bufferedMortalityInfrastructureGeoJsonOptionsStyle" />
      <l-control-scale position="bottomright" />
      <l-control v-if="zoom < 10" class="leaflet-control" position="bottomright">
        <v-alert density="compact" type="warning" title="Information" text="Zoomez pour
        afficher
        les données" />
      </l-control>
      <l-control-layers />
    </template>
    <utils-map-actions-menu v-if="!editMode" />
  </l-map>
</template>

<script setup lang="ts">
import leaflet from 'leaflet'
import { storeToRefs } from 'pinia';
import "leaflet.locatecontrol"
import 'leaflet.locatecontrol/dist/L.Control.Locate.min.css'
import { OpenStreetMapProvider, GeoSearchControl } from "leaflet-geosearch"
import "leaflet-geosearch/assets/css/leaflet.css"
import { LMap, LTileLayer, LGeoJson, LControlLayers, LControl, LControlScale } from "@vue-leaflet/vue-leaflet";
import buffer from '@turf/buffer'
import type { Feature, FeatureCollection } from "geojson"
import type { StoreGeneric } from "pinia"
import type { Layer, LatLng } from "leaflet";
import { computed, ref } from 'vue';

await import("@geoman-io/leaflet-geoman-free");

// Props
const { editMode, mode } = defineProps({
  editMode: Boolean,
  mode: { type: String, default: null },
})


// Stores
const cableStore: StoreGeneric = useCablesStore()
const mortalityStore: StoreGeneric = useMortalityStore()
const mapLayersStore: StoreGeneric = useMapLayersStore()
const coordinatesStore: StoreGeneric = useCoordinatesStore()

// Data
const map: Ref<typeof LMap | null> = ref(null)
const mapObject: Ref<typeof LMap | null> = ref(null)
const createLayer: Ref<Layer | null> = ref(null)
const mapReady: Ref<boolean> = ref(false)
const router = useRouter()
const externalSourceDataZoomTreshold = 13
const infrastructureLayersReady: Ref<boolean> = ref(false)
const otherNetworksLayersReady: Ref<boolean> = ref(false)
const bufferedSelectedInfrastructure: Ref<Feature | null> = ref(null)
const bufferedMortalityInfrastructure: Ref<Feature | null> = ref(null)
const enedisIsVisible = ref(false)
const rteIsVisible = ref(false)

const {
  zoom,
  center,
  bbox,
  selectedFeature,
  newGeoJSONObject,
  mortalityGetInfrastructure,
  mortalityInfrastructure,
} = storeToRefs(coordinatesStore)
const {
  infstrData,
  infstrDataLoadingStatus,
  pointData,
  opData,
  operatedPointData,
  lineStringData,
  operatedLineStringData,
  enedisInfrastructure,
  rteInfrastructure,
} = storeToRefs(cableStore)
const { mortalityData } = storeToRefs(mortalityStore)
const { baseLayers } = storeToRefs(mapLayersStore)

const iconDict: { [key: string]: string } = {
  COD_EL: 'lightning-bolt',
  COD_IM: 'star',
  COD_UNKNOWN: 'help',
}
const levelNotes: { [key: string]: number } = { 'RISK_L': 1, 'RISK_M': 2, 'RISK_H': 3 }
const rteColor: string = '#00838F' // Vuetify cyan-darken-3
const enedisColor: string = '#2E7D32' // Vuetify green-darken-3

const infraStructureLayers = computed(() => [
  {
    data: lineStringData.value,
    options: infrastructureGeoJsonOptions,
    name: 'Lignes',
    optionsStyle: infrastructureGeoJsonOptionsStyle
  },
  {
    data: pointData.value,
    options: infrastructureGeoJsonOptions,
    name: 'Supports',
    optionsStyle: null
  },
])

const operatedInfraStructureLayers = computed(() => [
  {
    data: operatedPointData.value,
    options: operatedInfrastructureGeoJsonOptions,
    optionsStyle: operatedInfrastructureGeoJsonOptionsStyle,
    name: 'Supports neutralisés',
  },
  {
    data: operatedLineStringData.value,
    options: operatedInfrastructureGeoJsonOptions,
    optionsStyle: operatedInfrastructureGeoJsonOptionsStyle,
    name: 'Lignes neutralisées',
  }
])

const otherNetworksLayers = computed(() => [
  {
    visible: enedisIsVisible.value,
    data: enedisInfrastructure.value,
    options: enedisInfrastructureGeoJsonOptions,
    optionsStyle: enedisInfrastructureGeoJsonOptionsStyle,
    name: 'Réseau ENEDIS',
  },
  {
    visible: rteIsVisible.value,
    data: rteInfrastructure.value,
    options: rteInfrastructureGeoJsonOptions,
    optionsStyle: rteInfrastructureGeoJsonOptionsStyle,
    name: 'Réseau RTE',
  },
])

const validInfrastructuresLayers = computed(() => {
  return infraStructureLayers.value.filter(layer => {
    return isValidFeatureCollection(layer.data)
  });
});

const validOperatedInfrastructuresLayers = computed(() => {
  return operatedInfraStructureLayers.value.filter(layer => {
    return isValidFeatureCollection(layer.data)
  });
});

const validOtherNetworksLayers = computed(() => {
  return otherNetworksLayers.value.filter(layer => {
    return isValidFeatureCollection(layer.data)
  });
});

const infrastructurePopupContent = (feature) => `
  <div>
    <h2>
      <span class="mdi ${feature.geometry.type === 'Point' ? 'mdi-transmission-tower' : 'mdi-cable-data'}">
        </span><span id="routerLink" style="cursor: pointer">${feature.geometry.type === 'Point' ? 'Poteau' : 'Tronçon'}
          ${feature.properties?.owner?.label} ${feature.properties?.id}</span>
    </h2>
    <button class="v-btn v-btn--slim w-100 v-theme--light bg-success v-btn--density-default v-btn--size-default v-btn--variant-flat" type="button"  id="MapInfrstrPopupLink" data-route="/infrastructure/${feature.properties.id}">
      Fiche support
    </button>
  </div>
`

const mortalityPopupContent = (feature) => `
  <div>
    <h2>
      <span class="text-red mdi mdi-${iconDict[feature.properties?.death_cause?.code] || 'help'}">
        ${feature.properties.species?.vernacular_name || feature.properties.species?.scientific_name}
    </h2>
    <p>${feature.properties?.death_cause?.label} - ${feature.properties?.date}</p>
    <button class="v-btn v-btn--slim w-100 v-theme--light bg-success v-btn--density-default v-btn--size-default v-btn--variant-flat" type="button" id="MapMortalityPopupLink" data-route="/mortality/${feature.id}">
      Fiche mortalité
    </button>
  </div>
`

const isValidFeatureCollection = (obj: any): obj is FeatureCollection => {
  return (
    obj &&
    obj.type === "FeatureCollection" &&
    Array.isArray(obj.features) &&
    obj.features.every((feature: any) =>
      feature.type === "Feature" &&
      feature.geometry &&
      typeof feature.properties === "object"
    )
  );
}

const infrastructureOnEachFeature = (feature: CablesFeature, layer: Layer) => {
  if (!mortalityGetInfrastructure.value) {
    if (feature.resourcetype?.endsWith('Operation')) {
      console.log('prepare popup')
      feature = infstrData.value.features.find(item => item.id = feature.properties?.infrastructure)
    }
    layer.bindPopup(infrastructurePopupContent(feature))
    layer.on('popupopen', () => {
      const id = feature?.properties?.id
      const link = document.getElementById('MapInfrstrPopupLink');
      link?.addEventListener('click', (event) => {
        event.preventDefault(); // Prevent the default anchor behavior
        if (['Point', 'Line'].includes(feature?.resourcetype) && !!id) {
          router.push(`/infrastructures/${id}`)
        }
      });
    });
  }
  layer.on('click', () => {
    if (mortalityGetInfrastructure.value) {
      mortalityInfrastructure.value = feature
      mortalityGetInfrastructure.value = !mortalityGetInfrastructure.value
    }
    else {
      selectedFeature.value = feature
    }
  })

}

const mortalityOnEachFeature = (feature: Feature, layer: Layer) => {
  if (!mortalityGetInfrastructure.value) {
    layer.bindPopup(mortalityPopupContent(feature))
    layer.on('popupopen', () => {
      const id = feature?.id
      const link = document.getElementById('MapMortalityPopupLink');
      link?.addEventListener('click', (event) => {
        event.preventDefault(); // Prevent the default anchor behavior
        router.push(`/mortality/${id}`)
      });
    });
  }
}


const infrastructureGeoJsonOptions = () => {
  return {
    onEachFeature: infrastructureOnEachFeature,
    pointToLayer: (feature: Feature, latlng: LatLng | null) => {
      if (latlng) {
        return leaflet.circleMarker(latlng, {
          radius: 6,
          fillColor: supportColor(feature),
          color: '#000',
          weight: 0.5,
          opacity: 0.5,
          fillOpacity: 0.8,
        })
      }
    }
  }
}


const operatedInfrastructureGeoJsonOptions = () => {
  return {
    onEachFeature: infrastructureOnEachFeature,
    pointToLayer: (_feature: Feature, latlng: LatLng | null) => {
      if (latlng) {
        return leaflet.circleMarker(latlng, {
          radius: 3,
          fillColor: '#00ff00',
          color: '#000',
          weight: 0,
          opacity: 1,
          fillOpacity: 0.8,
        })
      }
    }
  }
}



const mortalityGeoJsonOptions = () => {
  return {
    onEachFeature: mortalityOnEachFeature,
    pointToLayer: (feature: Feature, latlng: LatLng) => {
      if (latlng) {
        const icon = iconDict[feature.properties?.death_cause?.code] || 'help';
        const deathCaseIcon = leaflet.divIcon({
          html: `<span class="mdi mdi-${icon}"></span>`,
          iconSize: [15, 15],
          className: 'mapMarkerIcon'
        }
        );
        return leaflet.marker(latlng, { icon: deathCaseIcon });
      }
    }
  }
}


const enedisInfrastructureGeoJsonOptions = () => {
  return {
    pointToLayer: (_feature: Feature, latlng: LatLng | null) => {
      if (latlng) {
        return leaflet.circleMarker(latlng, {
          radius: 2,
          fillColor: enedisColor,
          color: enedisColor,
          weight: 0.5,
          opacity: 0.5,
          fillOpacity: 0.8,
        })
      }
    }
  }
}



const rteInfrastructureGeoJsonOptions = () => {
  return {
    pointToLayer: (_feature: Feature, latlng: LatLng | null) => {
      if (latlng) {
        return leaflet.circleMarker(latlng, {
          radius: 3,
          fillColor: rteColor,
          color: rteColor,
          weight: 0.5,
          opacity: 0.5,
          fillOpacity: 0.8,
        })
      }
    }
  }
}

// Layers OptionsStyles

const infrastructureGeoJsonOptionsStyle = (feature: Feature) => {
  return {
    color: lineColor(feature),
    weight: 5,
  }
}


const operatedInfrastructureGeoJsonOptionsStyle = (feature: Feature) => {
  return {
    color: '#00ff00',
    weight: 2,
  }
}


const enedisInfrastructureGeoJsonOptionsStyle = () => {
  return {
    color: enedisColor,
    opacity: 0.8,
    weight: 1.5,
    dashArray: '7, 3, 3, 3'
  }
}


const bufferedMortalityInfrastructureGeoJsonOptionsStyle = (_feature: Feature) => {
  const color = 'red'
  return {
    color: color,
    fillColor: color,
    weight: 2,
    opacity: 0.5,
  }
}

const bufferedSelectedInfrastructureGeoJsonOptionsStyle = (_feature: Feature) => {
  return {
    color: '#03A9F4',
    fillColor: '#03A9F4',
    weight: 2,
    opacity: 0.5,
  }
}

const rteInfrastructureGeoJsonOptionsStyle = () => {
  return {
    color: rteColor,
    opacity: 0.8,
    weight: 2,
    dashArray: '10, 10'
  }
}

// Watchers

// watch(selectedFeature, (newVal, oldVal) => {
//   if (JSON.stringify(newVal) !== JSON.stringify(oldVal)) {
//     const newObj = leaflet.geoJSON(newVal)
//     mapObject.value?.setView(newObj.getBounds().getCenter(), 15)
//   }
// })

watch(createLayer, (newLayer, _oldLayer) => {
  if (newLayer && newLayer.toGeoJSON()) {
    newGeoJSONObject.value = newLayer.toGeoJSON()
  } else {
    console.debug('Unique layer removed');
  }
});

watch(selectedFeature, (newVal, _oldVal) => {
  bufferedSelectedInfrastructure.value = newVal ? buffer(newVal, 150, { units: 'meters' }) : null
})

watch(mortalityInfrastructure, (newVal, _oldVal) => {
  bufferedMortalityInfrastructure.value = newVal ? buffer(newVal, 50, { units: 'meters' }) : null
})

const debounce = (func, delay) => {
  let timeout;
  return function (...args) {
    const context = this;
    clearTimeout(timeout);
    timeout = setTimeout(() => func.apply(context, args), delay);
  };
}

const handleBBox = debounce((bbox) => {
  cableStore.cancelRequest();
  mortalityStore.cancelRequest();

  if (zoom.value >= 10) {
    cableStore.getAllInfrastructureData({ in_bbox: bbox })
    mortalityStore.getMortalityData({ in_bbox: bbox })
  } else {
    infstrDataLoadingStatus.value = false
    infstrData.value = {}
    opData.value = {}
    mortalityData.value = {} as FeatureCollection
  }
  if (zoom.value >= externalSourceDataZoomTreshold) {
    cableStore.getEnedisInfrastructure(reverseBBoxString(mapObject.value.getBounds()))
    cableStore.getRteInfrastructure(reverseBBoxString(mapObject.value.getBounds()))
  } else {
    enedisInfrastructure.value = {} as FeatureCollection
    rteInfrastructure.value = {} as FeatureCollection
  }
}, 1000); // Adjust the delay as needed


watch(bbox, (newVal, _oldVal) => {
  handleBBox(newVal)
})


// helpers functions
const getBbox = () => {
  if (mapObject.value) {
    zoom.value = mapObject.value.getZoom()
    center.value = mapObject.value.getCenter()
    bbox.value = mapObject.value.getBounds().toBBoxString()
  }
}


const hookUpDraw = async () => {
  mapObject.value = map.value?.leafletObject;

  if (mapObject.value) {
    mapReady.value = true;

    // GeoLocate plugin
    leaflet.control.locate({ icon: 'mdi mdi-crosshairs-gps' }).addTo(mapObject.value)

    // GeoSearch plugin
    const provider = new OpenStreetMapProvider()
    GeoSearchControl({
      provider,
    }).addTo(mapObject.value)

    if (mapObject.value && editMode) {
      mapObject.value.pm.addControls({
        position: 'topleft',
        drawMarker: mode === 'point',
        drawCircleMarker: mode === 'circle-marker',
        drawPolyline: mode === 'line',
        drawPolygon: mode === 'polygon',
        drawRectangle: mode === 'rectangle',
        drawCircle: mode === 'circle',
        drawText: false,
        editMode: false,
        dragMode: false,
        removalMode: false,
        cutPolygon: false,
        rotateMode: false,
      })
      mapObject.value.pm.setPathOptions({
        color: '#ba02f2',
        fillColor: '#ba02f2',
        fillOpacity: 0.4,
      })
      mapObject.value.on('pm:create', (e) => {
        if (createLayer.value) {
          mapObject.value.removeLayer(createLayer.value);
        }
        createLayer.value = e.layer
        if (createLayer.value) {
          mapObject.value?.pm.disableDraw()
          mapObject.value?.pm.addControls({
            drawMarker: false,
            dragMode: mode === 'point' ? true : false,
            drawPolyline: false,
            editMode: mode === 'line' ? true : false,
            removalMode: true,
          })
        }
      }
      )
      mapObject.value.on('pm:remove', (e) => {
        if (createLayer.value === e.layer) {
          createLayer.value = null; // Clear the unique layer reference
        }
      })
      mapObject.value.on('pm:edit', (e) => {
        // Trigger a change in the uniqueLayer reference
        console.debug('edit', e)
        createLayer.value = mapObject.value.geoJSON(createLayer.value.toGeoJSON());
      })
      mapObject.value.on('pm:update', (e) => {
        // Trigger a change in the uniqueLayer reference
        console.debug('update', e)
        createLayer.value = mapObject.value.geoJSON(createLayer.value.toGeoJSON());
      })
    }
  }
};

const lineColor = (feature: Feature) => {
  const lastDiag = feature.properties?.diagnosis[0]
  if (lastDiag) {
    const sgmt_moving_risk = lastDiag.sgmt_moving_risk?.code
    const sgmt_landscape_integr_risk = lastDiag.sgmt_landscape_integr_risk?.code
    const sgmt_topo_integr_risk = lastDiag.sgmt_topo_integr_risk?.code
    const note = levelNotes[sgmt_moving_risk] + levelNotes[sgmt_landscape_integr_risk] + levelNotes[sgmt_topo_integr_risk]
    if (note < 4) {
      return 'blue'
    }
    if (note >= 4 && note < 7) {
      return 'orange'
    }
    else { return 'red' }
  }
  return 'grey'
}

const supportColor = (feature: Feature) => {
  const lastDiag = feature.properties?.diagnosis[0]
  if (lastDiag && lastDiag.pole_attractivity && lastDiag.pole_attractivity) {
    const attractivity = lastDiag.pole_attractivity.code
    const dangerousness = lastDiag.pole_attractivity.code
    const note = levelNotes[attractivity] + levelNotes[dangerousness]
    if (note == 2) {
      return 'blue'
    }
    if (note > 2 && note < 5) {
      return 'orange'
    }
    else { return 'red' }
  }
  return 'grey'
}

const reverseBBoxString = (bounds) => {
  const coords: Array<number> = [bounds.getSouth(), bounds.getWest(), bounds.getNorth(), bounds.getEast()]
  return coords.toString()
}

</script>

<style>
#map {
  width: 100%;
}

.mapMarkerIcon {
  text-align: center;
  /* Horizontally center the text (icon) */
  line-height: 15px;
  /* Vertically center the text (icon) */
  color: white;
  font-size: 15px;
  background-color: red;
  border-radius: 50%;
}
</style>
