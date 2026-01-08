<template>
  <l-map id="map" ref="map" class="d-flex" :zoom="zoom" :center="center" @ready="hookUpDraw" @zoom="getBbox"
    @moveend="getBbox">
    <template v-if="mapReady">
      <l-tile-layer v-for="baseLayer in baseLayers" :key="baseLayer.id" :name="baseLayer.name" :url="baseLayer.url"
        :visible="baseLayer.default" :attribution="baseLayer.attribution" :layer-type="baseLayer.layer_type" />
      <template v-f="otherNetworksLayersReady = true">
        <l-geo-json v-for="(layer, index) in validInfrastructuresLayers" :key='index' :geojson="layer.data"
          :ref="layer.ref" :options="layer.options(layer.data)" :options-style="layer.optionsStyle" :name="layer.name"
          layer-type="overlay" @ready="infrastructureLayersReady = true" />
      </template>
      <template v-if="infrastructureLayersReady">
        <l-geo-json v-for="(layer, index) in validOperatedInfrastructuresLayers" :key='index' :geojson="layer.data"
          :ref="layer.ref" :options="layer.options(layer.data)" :options-style="layer.optionsStyle" :name="layer.name"
          layer-type="overlay" />
      </template>
      <!-- <l-geo-json v-if="municipalities && !(Object.keys(municipalities).length === 0)" :geojson="municipalities"
        name="Communes" layer-type='overlay' :options="municipalitiesGeoJsonOptions" ref="municipalities"
        :options-style="municipalitiesOptionsStyle" @update:visible="municipalitesVisibleEvent"
        :visible="municipalitiesVisible">
      </l-geo-json> -->
      <l-geo-json v-for="(layer, index) in validOtherNetworksLayers" :key='index' :geojson="layer.data" :ref="layer.ref"
        :options="layer.options(layer.data)" :options-style="layer.optionsStyle" :name="layer.name" layer-type='overlay'
        @ready="otherNetworksLayersReady = true" :visible="layer.visible" />
      <l-geo-json v-if="isValidFeatureCollection(mortalityData)" name="Mortalité" layer-type="overlay" ref="mortality"
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
import { OpenStreetMapProvider, GeoSearchControl } from "leaflet-geosearch"
import { LMap, LTileLayer, LGeoJson, LControlLayers, LControl, LControlScale } from "@vue-leaflet/vue-leaflet";
import buffer from '@turf/buffer'
import type { BBox, Feature, FeatureCollection, GeometryObject } from "geojson"
import type { StoreGeneric } from "pinia"
import type { Layer, Map, LatLng, LatLngBounds, Polyline, Marker } from "leaflet";
import { computed, ref, type Reactive, type Ref } from 'vue';
import type { MortalityFeature } from '~/types/mortality';
import type { CablesFeature, NetworkFeatureCollection, NetworkFeature, NewLayerType } from '~/types/cables';
// import 'leaflet.control.layers.tree';
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
const globalStore: StoreGeneric = useGlobalStore()
const geoAreasStore: StoreGeneric = useGeoAreasStore()
// Data
const map: Ref<Map | null> = ref(null)
const mapObject: Ref<typeof LMap | null> = ref(null)
// const createLayer: Reactive<NewLayerType> = reactive({} as NewLayerType)
const createLayer: Ref<NewLayerType | null> = ref(null)
//const createLayer: Reactive<Layer> = reactive({} as Layer)
const mapReady: Ref<boolean> = ref(false)
const router = useRouter()
const externalSourceDataZoomTreshold = 13
const infrastructureLayersReady: Ref<boolean> = ref(false)
const otherNetworksLayersReady: Ref<boolean> = ref(false)
const bufferedSelectedInfrastructure: Ref<Feature<GeometryObject> | undefined> = ref(undefined)
const bufferedMortalityInfrastructure: Ref<Feature<GeometryObject> | undefined> = ref(undefined)
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
const { refreshData } = storeToRefs(globalStore)
// const { municipalities, municipalitiesVisible } = storeToRefs(geoAreasStore)

const iconDict: { [key: string]: string } = {
  COD_EL: 'lightning-bolt',
  COD_IM: 'star',
  COD_UNKNOWN: 'help',
}
const levelNotes: { [key: string]: number } = { 'RISK_L': 1, 'RISK_M': 2, 'RISK_H': 3 }
const rteColor: string = '#00838F' // Vuetify cyan-darken-3
const enedisColor = (item: NetworkFeature) => item.properties.type === 'Underground' ? 'rgba(46,125,50,0.6)' : 'rgba(46,125,50,1)' // Vuetify green-darken-3
const enedisDash = (item: NetworkFeature) => item.properties.type === 'Underground' ? '3, 7, 3, 7' : '7, 3, 3, 3'

const baseTree = [
  {
    label: 'Test',
    children: [
      { label: 'mortality', layer: 'mortality' },
      { label: 'municipality', layer: 'municipality' },
    ],
  },
];

const infraStructureLayers = computed(() => [
  {
    data: lineStringData.value,
    options: infrastructureGeoJsonOptions,
    name: 'Lignes',
    optionsStyle: infrastructureGeoJsonOptionsStyle,
    ref: 'lines'
  },
  {
    data: pointData.value,
    options: infrastructureGeoJsonOptions,
    name: 'Supports',
    optionsStyle: null,
    ref: 'supports'
  },
])

const operatedInfraStructureLayers = computed(() => [
  {
    data: operatedPointData.value,
    options: operatedInfrastructureGeoJsonOptions,
    optionsStyle: operatedInfrastructureGeoJsonOptionsStyle,
    name: 'Supports neutralisés',
    ref: 'operated_support',
  },
  {
    data: operatedLineStringData.value,
    options: operatedInfrastructureGeoJsonOptions,
    optionsStyle: operatedInfrastructureGeoJsonOptionsStyle,
    name: 'Lignes neutralisées',
    ref: 'operated_line'
  }
])

const otherNetworksLayers = computed(() => [
  {
    visible: enedisIsVisible.value,
    data: enedisInfrastructure.value,
    options: enedisInfrastructureGeoJsonOptions,
    optionsStyle: enedisInfrastructureGeoJsonOptionsStyle,
    name: 'Réseau ENEDIS',
    ref: 'hta_bt'
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

const infrastructurePopupContent = (feature: CablesFeature) => `
  <div>
    <h2>
      <span class="mdi ${feature.geometry.type === 'Point' ? 'mdi-transmission-tower' : 'mdi-cable-data'}"> <span class="text-disabled">${feature.properties?.id}</span> • 
        </span><span id="routerLink" style="cursor: pointer">${feature.geometry.type === 'Point' ? 'Poteau' : 'Tronçon'}
          ${feature.properties?.network_type?.code} </span>
    </h2>
    <button class="v-btn v-btn--slim w-100 v-theme--light bg-success v-btn--density-default v-btn--size-default v-btn--variant-flat" type="button"  id="MapInfrstrPopupLink" data-route="/infrastructure/${feature.properties.id}">
      <span class="mdi mdi-eye"> Voir la fiche
    </button>
  </div>
`

const mortalityPopupContent = (feature: MortalityFeature) => `
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

const mortalityOnEachFeature = (feature: MortalityFeature, layer: Layer) => {
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



// const municipalitiesOnEachFeature = (feature: Feature, layer: Layer) => {

//   // layer.bindTooltip(feature.properties?.name)
//   console.log('<municipalitiesOnEachFeature>', feature)
//   layer.bindTooltip("Hello", {});
// }


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
    pointToLayer: (feature: NetworkFeature, latlng: LatLng | null) => {
      if (latlng) {
        return leaflet.circleMarker(latlng, {
          radius: 2,
          fillColor: enedisColor(feature),
          color: enedisColor(feature),
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


// const municipalitiesGeoJsonOptions = () => {
//   return {
//     onEachFeature: municipalitiesOnEachFeature,
//   }
// }


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


const enedisInfrastructureGeoJsonOptionsStyle = (feature: NetworkFeature) => {
  return {
    color: enedisColor(feature),
    opacity: 1,
    weight: 1.5,
    dashArray: enedisDash(feature)
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

// const municipalitiesOptionsStyle = (_feature: Feature) => {
//   return {
//     color: '#333',
//     fillColor: '#000',
//     weight: 1,
//     opacity: 0.7,
//     fillOpacity: 0,
//   }
// }


// const municipalitesVisibleEvent = (visibility) => {
//   municipalitiesVisible.value = visibility;
// }
// Watchers

const displaySelectedFeature = (feature: Feature) => {
  const newObj = leaflet.geoJSON(feature)
  mapObject.value?.setView(newObj.getBounds().getCenter(), 15)
  bufferedSelectedInfrastructure.value = buffer(feature, 150, { units: 'meters' })
  console.log('selectedFeature feature', newObj, Object.keys(newObj), isLayer(newObj))
}

watch(selectedFeature, (newVal, oldVal) => {
  if (JSON.stringify(newVal) !== JSON.stringify(oldVal)) {
    displaySelectedFeature(newVal)
    console.log('selectedFeature newVal', newVal, Object.keys(newVal), isLayer(newVal))
  }
})

function isLayer(layer: Layer): layer is Layer {
  try {
    return 'toGeoJSON' in layer;
  } catch (error: any) {
    console.error("An error Occured: ", error.message);
  }
  return false
}

watch(createLayer, (newLayer: NewLayerType, _oldLayer) => {
  console.log('watcher createLayer', newLayer, typeof newLayer, isLayer(newLayer))
  if (newLayer && isLayer(newLayer)) {
    console.log('set NewGeoJSONObject value')
    newGeoJSONObject.value = newLayer.toGeoJSON()
  } else {
    console.debug('Unique layer removed');
    // mapObject.value?.pm.disableDraw()
    mapObject.value?.pm.addControls({
      drawMarker: mode === 'point',
      drawCircleMarker: mode === 'circle-marker',
      drawPolyline: mode === 'line',
      drawPolygon: mode === 'polygon',
      drawRectangle: mode === 'rectangle',
      drawCircle: mode === 'circle',
      editMode: false,
      removalMode: false,
      dragMode: false,
    })
  }
});

// watch(selectedFeature.value, (newVal, _oldVal) => {
//   if (newVal) {
//     bufferedSelectedInfrastructure.value = buffer(newVal, 150, { units: 'meters' })
//   }
// })

watch(mortalityInfrastructure, (newVal, _oldVal) => {
  if (newVal) {
    bufferedMortalityInfrastructure.value = buffer(newVal, 50, { units: 'meters' })
  }
})

// const debounce = (func: Function, delay: number) => {
//   let timeout: NodeJS.Timeout | number;
//   return function (...args) {
//     const context: any = this;
//     clearTimeout(timeout);
//     timeout = setTimeout(() => func.apply(context, args), delay);
//   };
// }
const debounce = <T extends (...args: any[]) => any>(func: T, delay: number) => {
  let timeout: ReturnType<typeof setTimeout>;

  return function (this: any, ...args: Parameters<T>) {
    clearTimeout(timeout);
    timeout = setTimeout(() => func.apply(this, args), delay);
  };
};

const handleBBox = debounce((bbox: BBox) => {
  cableStore.cancelRequest();
  mortalityStore.cancelRequest();

  if (zoom.value >= 10) {
    const params = { in_bbox: bbox }
    cableStore.getAllInfrastructureData(params);
    mortalityStore.getMortalityData(params);
    geoAreasStore.getMunicipalities(params);
  } else {
    infstrDataLoadingStatus.value = false;
    infstrData.value = {};
    opData.value = {};
    mortalityData.value = {} as FeatureCollection;
    // municipalities.value = {} as FeatureCollection;
  }

  if (zoom.value >= externalSourceDataZoomTreshold && mapObject.value) {
    cableStore.getEnedisInfrastructure(reverseBBoxString(mapObject.value.getBounds()));
    //cableStore.getRteInfrastructure(reverseBBoxString(mapObject.value.getBounds()));
  } else {
    enedisInfrastructure.value = {} as NetworkFeatureCollection;
    //rteInfrastructure.value = {} as NetworkFeatureCollection;
  }

  // let overlays = {};

  // // Use map.eachLayer to generate overlays
  // mapObject.value.eachLayer((layer) => {
  //   if (layer instanceof L.Marker) {
  //     overlays["Marker"] = layer;
  //   }
  //   if (layer instanceof L.Circle) {
  //     overlays["Circle"] = layer;
  //   }
  // });

  // // Add the control layer
  // const treeControl = L.control.layers.tree(overlays, {
  //   closedSymbol: '►',
  //   openedSymbol: '▼'
  // }).addTo(mapObject.value);
}, 1000);

// Watch for changes in bbox
watch(bbox, (newVal, _oldVal) => {
  handleBBox(newVal);
});


watch(refreshData, (newVal, _oldVal) => {
  console.log('watch refreshData', newVal, newVal.value)
  if (newVal == true) {
    handleBBox(bbox.value)
    refreshData.value = false
  }
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

    // const treeControl = L.control.layers.tree(baseTree).addTo(mapObject.value);

    console.log('mapObject.value', mapObject.value)



    // GeoSearch plugin
    const provider = new OpenStreetMapProvider()
    GeoSearchControl({
      provider,
    }).addTo(mapObject.value)

    if (mapObject.value && editMode) {
      console.log('editMode & mode', editMode, mode)
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
      mapObject.value.on('pm:create', ({ layer }: { layer: NewLayerType }) => {
        if (createLayer) {
          mapObject.value?.removeLayer(createLayer);
        }
        layer.on('pm:dragdisable', ({ layer }: { layer: NewLayerType }) => {
          newGeoJSONObject.value = layer.toGeoJSON()
        })
        layer.on('pm:remove', ({ layer }: { layer: NewLayerType }) => {
          newGeoJSONObject.value = null
        })
        newGeoJSONObject.value = layer.toGeoJSON()
        createLayer.value = layer
        layer.on('pm:dragdisable', ({ layer }: { layer: NewLayerType }) => {
          newGeoJSONObject.value = layer.toGeoJSON()
        })
        // Object.assign(createLayer, layer)
        if (layer) {
          mapObject.value?.pm.disableDraw()
          mapObject.value?.pm.addControls({
            drawMarker: false,
            drawPolyline: false,
            dragMode: mode === 'point' ? true : false,
            editMode: mode === 'line' ? true : false,
            removalMode: true,
          })
        }
      })
      createLayer.value?.on('pm:drag', ({ layer }: { layer: NewLayerType }) => {
        newGeoJSONObject.value = layer.toGeoJSON()
        console.log('layer pm:drag', newGeoJSONObject.value)
      })
      // mapObject.value.on('pm:drag', ({ layer }: { layer: NewLayerType }) => {
      //   newGeoJSONObject.value = layer.toGeoJSON()
      //   console.log('pm:drag', newGeoJSONObject.value)
      // })
      mapObject.value.on("pm:globalremovalmodetoggled", ({ layer }: { layer: NewLayerType }) => {
        console.log('pm:globalremovalmodetoggled', layer);
      });
      mapObject.value.on('pm:drawend', ({ layer }: { layer: NewLayerType }) => {
        console.log('pm:drawend', layer)
      })
      // mapObject.value.on('pm:dragend', ({ layer }: { layer: NewLayerType }) => {
      //   console.log('pm:dragend', layer)
      // })
      // mapObject.value.on('pm:dragstart', ({ layer }: { layer: NewLayerType }) => {
      //   console.log('pm:dragstart', layer)
      // })
      mapObject.value.on('pm:update', ({ layer }: { layer: NewLayerType }) => {
        console.log('pm:update', layer)
      })
      mapObject.value.on('pm:cancel', ({ layer }: { layer: NewLayerType }) => {
        console.log('pm:cancel', layer)
      })
      mapObject.value.on('pm:change', ({ layer }: { layer: NewLayerType }) => {
        newGeoJSONObject.value = layer.toGeoJSON()
        console.log('pm:change', newGeoJSONObject.value)
      })
      mapObject.value.on('pm:remove', ({ layer }: { layer: NewLayerType }) => {
        newGeoJSONObject.value = null;
        createLayer.value = null;
        console.log('map pm:remove', layer, newGeoJSONObject.value, createLayer.value)
        mapObject.value?.pm.globalDrawModeEnabled();
        // mapObject.value?.pm.removeControls({
        //   drawMarker: false,
        //   drawPolyline: false,
        //   dragMode: mode === 'point' ? true : false,
        //   editMode: mode === 'line' ? true : false,
        //   removalMode: true,
        // })

      })
      // mapObject.value.on('pm:remove', ({ layer }: { layer: NewLayerType }) => {
      //   if (createLayer === layer) {
      //     Object.assign(createLayer, null); // Clear the unique layer reference
      //   }
      // })
      mapObject.value.on('pm:edit', ({ layer }: { layer: NewLayerType }) => {
        // Trigger a change in the uniqueLayer reference

        console.debug('edit', layer)
        Object.assign(createLayer, mapObject.value?.geoJSON(layer.toGeoJSON()));
      })
      mapObject.value.on('pm:update', ({ layer }: { layer: NewLayerType }) => {
        // Trigger a change in the uniqueLayer reference
        Object.assign(createLayer, mapObject.value?.geoJSON(layer.toGeoJSON()));
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

const reverseBBoxString = (bounds: LatLngBounds) => {
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
