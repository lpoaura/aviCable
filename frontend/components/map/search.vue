<template>
  {{ mode }}
  <l-map id="map" ref="map" class="d-flex" :zoom="zoom" :center="center" @ready="hookUpDraw" @zoom="getMapBounds"
    @moveend="getMapBounds">
    <!-- <l-map id="map" ref="map" class="d-flex align-stretch" :zoom="zoom" :center="center" @ready="hookUpDraw"> -->
    <template v-if="mapReady">
      <l-tile-layer v-for="baseLayer in baseLayers" :key="baseLayer.id" :name="baseLayer.name" :url="baseLayer.url"
        :visible="baseLayer.default" :attribution="baseLayer.attribution" :layer-type="baseLayer.layer_type" />

      <l-geo-json v-if="lineStringData" name="Réseaux cablés" layer-type="overlay" :geojson="lineStringData"
        :options="infrastructureGeoJsonOptions" :options-style="infrastructureGeoJsonOptionsStyle" />
      <l-geo-json v-if="pointData" name="Supports" layer-type="overlay" :geojson="pointData"
        :options="infrastructureGeoJsonOptions" />
      <l-geo-json v-if="mortalityData" name="Mortalité" layer-type="overlay" :geojson="mortalityData"
        :options="deathCasesGeoJsonOptions" />
      <l-geo-json v-if="selectedFeature" :geojson="selectedFeature" :options-style="selectedFeatureGeoJsonStyle" />
      <l-geo-json v-if="operatedLineStringData" name="Réseaux cablés" layer-type="overlay"
        :geojson="operatedLineStringData" :options="infrastructureGeoJsonOptions" />
      <l-geo-json v-if="pointData" name="Supports neutralisés" layer-type="overlay" :geojson="operatedPointData"
        :options="operatedInfrastructureGeoJsonOptions" />
      <l-geo-json v-if="newGeoJSONObject" :geojson="newGeoJSONObject" /> -->
      <l-wms-tile-layer
        url="https://data.lpo-aura.org/project/1851496a4547ac630b73c581d3f9b56f/?SERVICE=WMS&REQUEST=GetCapabilities"
        attribution="LPO AuRA" layer-type="base" name="CRA AuRA" version="1.3.0" format="image/png" :transparent="true"
        layers="osm,cra_aura_latest" :visible="false" />
      <l-control v-if="zoom < 10" class="leaflet-control" position="bottomright">
        <v-alert density="compact" type="warning" title="Information" text="Zoomez pour
        afficher
        les données" />
      </l-control>
      <l-control-layers />
      <l-control-scale position="bottomright" />

      <!-- <l-marker :lat-lng="center" ></l-marker> -->
      <!-- <l-geo-json v-if="mortalityItem" :geojson="mortalityItem" :options="deathCasesGeoJsonOptions" /> -->
    </template>
    <utils-map-actions-menu v-if="!editMode" />
  </l-map>
</template>

<script setup lang="ts">
import leaflet from 'leaflet'
import "leaflet.locatecontrol"
import 'leaflet.locatecontrol/dist/L.Control.Locate.min.css'
// import 'leaflet-search'
import { OpenStreetMapProvider, GeoSearchControl } from "leaflet-geosearch"
import "leaflet-geosearch/assets/css/leaflet.css"
import { LMap, LTileLayer, LMarker, LGeoJson, LControlLayers, LControl, LControlScale, LWmsTileLayer } from "@vue-leaflet/vue-leaflet";
// import { useMapLayersStore } from "store/mapLayersStore";
import buffer from '@turf/buffer'
import type { GeoJSON, Feature } from "geojson"
// import { useCablesStore } from "~/store/cablesStore"
import type { StoreGeneric } from "pinia"
import type {Map, PointTuple, GeoJSONOptions, Layer} from "leaflet";

// import { useCoordinatesStore } from "../store/coordinatesStore";

await import("@geoman-io/leaflet-geoman-free");

const {editMode, mode, mortalityItem} = defineProps({
  editMode: Boolean,
  mode: { type: String, default: null },
  mortalityItem: {} as Feature
})

const map : Ref<typeof LMap|null> = ref(null)
const mapObject : Ref<typeof LMap|null> = ref(null)
const createLayer: Ref<Layer |null> = ref(null)
const mapReady : Ref<boolean> = ref(false)
const router = useRouter()
// Stores
const cableStore : StoreGeneric  = useCablesStore()
const mortalityStore: StoreGeneric = useMortalityStore()
const mapLayersStore : StoreGeneric = useMapLayersStore()
const coordinatesStore : StoreGeneric = useCoordinatesStore()

const zoom : ComputedRef<number> = computed(() => coordinatesStore.zoom)
const center : ComputedRef<PointTuple> = computed<PointTuple>(() => coordinatesStore.center)

const pointData: ComputedRef<GeoJSON> = computed<GeoJSON>(() => cableStore.getPointDataFeatures)
const operatedPointData : ComputedRef<GeoJSON> = computed<GeoJSON>(() => cableStore.getOperatedPointDataFeatures)
const lineStringData: ComputedRef<GeoJSON> = computed<GeoJSON>(() => cableStore.getLineDataFeatures)
const operatedLineStringData: ComputedRef<GeoJSON> = computed<GeoJSON>(() => cableStore.getLineDataFeatures)
const mortalityData: ComputedRef<GeoJSON> = computed<GeoJSON>(() => mortalityStore.getMortalityFeatures)
const newGeoJSONPoint: ComputedRef<GeoJSON> = computed<GeoJSON>(() => coordinatesStore.newGeoJSONPoint)
// const mortalityItem:
const baseLayers = computed(() => mapLayersStore.baseLayers)

const selectedFeature : ComputedRef<GeoJSON|null> = computed<GeoJSON|null>(() =>
  !(Object.keys(coordinatesStore.selectedFeature).length === 0)
  ? buffer(coordinatesStore.selectedFeature, 150, {units: 'meters'})
  : null
)

const infrastructurePopupContent = (feature) => `<h2><span class="mdi ${feature.geometry.type === 'Point' ? 'mdi-transmission-tower':'mdi-cable-data'}">
      </span><span id="routerLink" style="cursor: pointer">${feature.geometry.type === 'Point' ? 'Poteau':'Tronçon'}
        ${feature.properties?.owner.label} ${feature.properties?.id}</span></h2>`

const infrastructureOnEachFeature = (feature : Feature, layer : Layer) => {
  layer.bindPopup(infrastructurePopupContent(feature))

    layer.on('popupopen', () => {
      const id = feature?.properties?.id
        const link = document.getElementById('routerLink');
        link.addEventListener('click', (event) => {
          event.preventDefault(); // Prevent the default anchor behavior
          if (['Point','Lines'].includes(feature?.resourcetype) && id) {
            router.push(`/${feature.resourcetype ==='Point'? 'supports':'lines'}/${id}`)
          }
        });
      });
}

const mortalityOnEachFeature = (feature : Feature, layer : Layer) => {
  // TODO To be adapted
  if (feature.properties) {
    layer.bindPopup(
      `<h2><span class="mdi mdi-coffin"></span><a to="/search#mortality">${feature.properties.species.vernacular_name}</a></h2>
      <i>${feature.properties.species.scientific_name}</i>
    <p><strong>Date</strong>&nbsp;:&nbsp;${feature.properties.date}<br>
        <strong>Cause</strong>&nbsp;:&nbsp;${feature.properties.death_cause.label}
      </dl>
      </p>`
    )
    layer.on('click', (e)=> {console.log('click', feature, e)})
  }
  // remove pm from layer to prevent action from geoman (no more drag/edit/remove ...)
  // console.log('layer', layer)
  // delete layer.pm
  // layer.setStyle({ pmIgnore: false })
}



const infrastructureGeoJsonOptions : GeoJSONOptions = reactive({
  onEachFeature : infrastructureOnEachFeature,
})

const operatedInfrastructureGeoJsonOptions : GeoJSONOptions = reactive({
  onEachFeature : infrastructureOnEachFeature,
})


const selectedFeatureGeoJsonOptions: GeoJSONOptions = reactive({})


// const selectedFeatureGeoJsonOptions : GeoJSONOptions = reactive({})


const deathCasesGeoJsonOptions : GeoJSONOptions = reactive({
  onEachFeature: mortalityOnEachFeature ,
})

// watch(mapObject, (newVal, oldVal) => {
//   console.log('mapObject watcher', mapObject.value.getBounds())
// })
watch(selectedFeature, (newVal, oldVal) => {
  if (JSON.stringify(newVal) !== JSON.stringify(oldVal)) {

    console.log('selectedFeature update')
    const newObj = leaflet.geoJSON(newVal)
    // const centroid = newVal.geometry.type == ''
    // coordinatesStore.setCenter(newObj.getBounds().getCenter())
    // coordinatesStore.setZoom(15)
    mapObject.value?.setView(newObj.getBounds().getCenter(), 15)
  }
})

watch(createLayer, (newLayer, oldLayer) => {
  if (newLayer) {
    console.log('Unique layer changed:', newLayer);
    // You can perform additional actions here based on the unique layer's changes
  } else {
    console.log('Unique layer removed');
  }
});

const getMapBounds = () => {
  // console.log(mapObject.value.getBounds().toBBoxString())
  if (mapObject.value) {
    coordinatesStore.setMapBounds(mapObject.value.getBounds().toBBoxString())
    coordinatesStore.setZoom(mapObject.value.getZoom())
    coordinatesStore.setCenter(mapObject.value.getCenter())
  }
}



const selectedFeatureGeoJsonStyle = (_feature: Feature) => {
  const color='red'
    return {
      color: color,
      fillColor: color,
      weight: 2,
      opacity: 0.5
    }
  }

  const infrastructureGeoJsonOptionsStyle = (feature: Feature, latlng : any ) => {
    return  {
      radius: 6,
      fillColor: levelColor(feature),
      color:  levelColor(feature),
      weight: 1,
      opacity: 1,
      fillOpacity: 0.8,
      // draggable: true,
    }
  }
const hookUpDraw = async () => {
  mapObject.value = map.value?.leafletObject;
  // console.log('mapObject.value', mapObject.value.getBounds(), map)
  mapReady.value = true;

  // GeoLocate plugin
  leaflet.control.locate({icon: 'mdi mdi-crosshairs-gps'}).addTo(mapObject.value)

  // GeoSearch plugin
  const provider = new OpenStreetMapProvider()
  GeoSearchControl({
    provider,
  }).addTo(mapObject.value)

  if (mapObject.value && editMode) {
// mapObject.value.addControl(
//   L.control.locate()
// )

    // mapObject.value.pm.setLang("en_gb");
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
          color: 'red',
          fillColor: 'red',
          fillOpacity: 0.4,
        })
    mapObject.value.on('pm:create', (e) => {
      if (createLayer.value) {
        mapObject.value.removeLayer(createLayer.value);
      }
      console.log('map on createLayer', e)
      console.log('createLayers before assign', createLayer, createLayer?.value)
          createLayer.value = e.layer
          console.log('createLayers after assign', createLayer, createLayer.value)
          if (createLayer.value){
            if (createLayer.value.toGeoJSON()) {
              coordinatesStore.setNewGeoJSONObject(
                createLayer.value.toGeoJSON()
              )
              mapObject.value?.pm.disableDraw()
              mapObject.value?.pm.addControls({
                drawMarker: false,
                dragMode: mode==='point' ? true : false,
                drawPolyline:false,
                editMode: mode === 'line' ? true : false,
                removalMode: true,
              })
            }
          }
          // // set listener on drag event on this layer
          // this.handleDrag(createLayer)

          // // in case of remove event, trigger handleRemove() method
          // e.layer.on('pm:remove', (_e) => {
          //   this.handleRemove()
          // })
        })
    // mapObject.value.on("pm:drawstart", ({ workingLayer, shape }) => {
    //   console.log('drawstart', workingLayer)
    //   workingLayer.on("pm:vertexadded", (e) => {
    //     console.log('vertexadded', e, shape);
    //     geofence.value.push(e)
    //   });
    // });

    // mapObject.value.on("pm:drawend", () => {
    //   console.log("drawend", geofence.value);
    // });
    mapObject.value.on('pm:remove', (e) => {
      if (createLayer.value === e.layer) {
        createLayer.value = null; // Clear the unique layer reference
        console.log('Layer removed:', e.layer);
      }
    })
    mapObject.value.on('pm:edit', (e) => {
    // Trigger a change in the uniqueLayer reference
    console.log('edit', e)
    createLayer.value = mapObject.value.geoJSON(createLayer.value.toGeoJSON());
  })
  mapObject.value.on('pm:update', (e) => {
    // Trigger a change in the uniqueLayer reference
    console.log('update', e)
    createLayer.value = mapObject.value.geoJSON(createLayer.value.toGeoJSON());
  })
  }
};

const levelColor = (feature: Feature) => {
  const lastDiag=feature.properties?.diagnosis[0]
  const levelNotes : {[key: string]: number} = {'RISK_L':1,'RISK_M':2,'RISK_H':3}
  if (lastDiag && lastDiag.pole_attractivity && lastDiag.pole_attractivity) {
    const attractivity = lastDiag.pole_attractivity.code
    const dangerousness = lastDiag.pole_attractivity.code
    const note = levelNotes[attractivity] + levelNotes[dangerousness]
    if (note == 2) {
      return 'blue'
    }
    if (note > 2 && note < 5)
    {
      return 'orange'
    }
    else {return 'red'}
  }
  return 'grey'
}

const abortController : Ref<AbortController | undefined> = ref<AbortController|undefined>(undefined)
const bbox : ComputedRef<string|null> = computed<string|null>(() => coordinatesStore.mapBounds)
    // const zoom : ComputedRef<number> = computed<number>(() => coordinatesStore.zoom)

watch(bbox, (newVal, _oldVal) => {
  console.log('zoom', zoom.value)
  console.log(abortController)
  if (abortController.value) {
    abortController.value.abort();
    console.log("Download aborted");
  }
  abortController.value = new AbortController()
  if (zoom.value >= 10) {
    cableStore.getInfrstrData({in_bbox: newVal}, abortController.value)
    mortalityStore.getMortalityData({in_bbox: newVal}, abortController.value)

  } else {
    cableStore.setInfrstrData({})
    cableStore.setInfrstrDataLoadingStatus(false)
    mortalityStore.setMortalityData({} as FeatureCollection)
  }
})

onBeforeMount(async () => {
  // const { circleMarker } = await import("leaflet/dist/leaflet-src.esm");
  infrastructureGeoJsonOptions.pointToLayer = (feature: Feature, latlng : any ) => {
    return leaflet.circleMarker(latlng, {
      radius: 6,
      fillColor: levelColor(feature),
      color: '#000',
      weight: 1,
      opacity: 1,
      fillOpacity: 0.8,
      // draggable: true,
    })
  }
  operatedInfrastructureGeoJsonOptions.pointToLayer = (_feature: Feature, latlng : any ) => {
    return leaflet.circleMarker(latlng, {
      radius: 3,
      fillColor: '#00ff00',
      color: '#000',
      weight: 0,
      opacity: 1,
      fillOpacity: 0.8,
      // draggable: true,
    })
  }

  selectedFeatureGeoJsonOptions.pointToLayer = (feature: Feature, latlng : any ) => {
    console.log('selectedFeatureGeoJsonOptions',feature, latlng)
    if (feature.resourcetype === 'Point') {
    return leaflet.circleMarker(latlng, {
      radius: 20,
      fillColor: 'red',
      color: 'red',
      weight: 1,
      opacity: 1,
      fillOpacity: 0.2,
      // draggable: true,
    })}
    else {
      return null
    }
  }



  deathCasesGeoJsonOptions.pointToLayer = (feature: Feature, latlng : any ) => {
    const iconDict : {[key: string]: string} = {
      COD_EL: 'lightning-bolt',
      COD_IM : 'star',
      COD_UNKNOWN: 'help',
    }
    const icon = iconDict[feature.properties?.death_cause?.code] || 'help';
    const deathCaseIcon = leaflet.divIcon({
      html: `<span class="mdi mdi-${icon}"></span>`,
      iconSize: [15, 15],
      className: 'mapMarkerIcon'}
      );
    return leaflet.marker(latlng, {icon: deathCaseIcon});

      // draggable: true,
    }
})

onMounted(() => {})

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
