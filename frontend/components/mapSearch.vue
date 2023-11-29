<template>
  <l-map id="map" ref="map" class="d-flex" :zoom="zoom" :center="center" @ready="hookUpDraw" @zoom="getMapBounds"
    @moveend="getMapBounds">
    <!-- <l-map id="map" ref="map" class="d-flex align-stretch" :zoom="zoom" :center="center" @ready="hookUpDraw"> -->
    <template v-if="mapReady">
      <l-tile-layer v-if="mapReady" v-for="baseLayer in baseLayers" :key="baseLayer.id" :name="baseLayer.name"
        :url="baseLayer.url" :visible="baseLayer.default" :attribution="baseLayer.attribution" layer-type="base" />
      <l-control-layers />
      <l-geo-json v-if="lineStringData" name="Réseaux cablés" layer-type="overlay" :geojson="lineStringData"
        :options="infrastructureGeoJsonOptions" />
      <l-geo-json v-if="pointData" name="Supports" layer-type="overlay" :geojson="pointData"
        :options="infrastructureGeoJsonOptions" />
      <l-geo-json v-if="mortalityData" name="Mortalité" :visible="false" layer-type="overlay" :geojson="mortalityData"
        :options="deathCasesGeoJsonOptions" />
      <l-control v-if="zoom < 9" class="leaflet-control leaflet-demo-control" position="bottomright">Zoomez pour afficher
        les données</l-control>
      <!-- <l-geo-json v-if="selectedFeature" :geojson="selectedFeature" /> -->
      <!-- <l-geo-json v-if="mortalityItem" :geojson="mortalityItem" :options="deathCasesGeoJsonOptions" /> -->
    </template>
    <utils-map-actions-menu v-if="!editMode" />
  </l-map>
</template>

<script setup lang="ts">
import leaflet from 'leaflet'
import "leaflet.locatecontrol";
import 'leaflet.locatecontrol/dist/L.Control.Locate.min.css'
import { LMap, LTileLayer, LGeoJson, LControlLayers, LControl } from "@vue-leaflet/vue-leaflet";
// import { useMapLayersStore } from "store/mapLayersStore";
import { GeoJSON, Feature } from "geojson"
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

const map = ref({})

const mapObject : Ref<null | Map> = ref({})
const createLayer: Ref<Layer |null> = ref(null)
const mapReady : Ref<Boolean> = ref(false)

// Stores
const cableStore : StoreGeneric  = useCablesStore()
const mortalityStore: StoreGeneric = useMortalityStore()
const mapLayersStore : StoreGeneric = useMapLayersStore()
const coordinatesStore : StoreGeneric = useCoordinatesStore()

const zoom : ComputedRef<number> = computed(() => coordinatesStore.zoom)
// const zoom : Ref<number> = ref<number>(() => coordinatesStore.zoom)
const center : ComputedRef<PointTuple> = computed<PointTuple>(() => coordinatesStore.center)
// const center : Ref<PointTuple>= ref([46.6423682169416,2.1940236627886227] as PointTuple);

const pointData: ComputedRef<GeoJSON> = computed<GeoJSON>(() => cableStore.getPointDataFeatures);
const lineStringData: ComputedRef<GeoJSON> = computed<GeoJSON>(() => cableStore.getLineDataFeatures);
const mortalityData: ComputedRef<GeoJSON> = computed<GeoJSON>(() => mortalityStore.getMortalityFeatures);
// const mortalityItem:
const baseLayers = computed(() => mapLayersStore.baseLayers)

const newPointCoord = computed(() => coordinatesStore.newPointCoord)
const newLineCoord = computed(() => coordinatesStore.newLineCoord)
const selectedFeature = computed(() => coordinatesStore.selectedFeature)

const infrastructureOnEachFeature = (feature : Feature, layer : any) => {
  // TODO To be adapted
  layer.bindPopup(
    `<h2><span class="mdi ${feature.geometry.type === 'Point' ? 'mdi-transmission-tower':'mdi-cable-data'}">
      </span><a to="/search#mortality">${feature.geometry.type === 'Point' ? 'Poteau':'Tronçon'} 
        ${feature.properties?.owner.label} ${feature.properties?.id}</a></h2>`
    )
  // remove pm from layer to prevent action from geoman (no more drag/edit/remove ...)
  // console.log('layer', layer)
  // delete layer.pm
  // layer.setStyle({ pmIgnore: false })
}

const mortalityOnEachFeature = (feature : Feature, layer : any) => {
  // TODO To be adapted
  layer.bindPopup(
    `<h2><span class="mdi mdi-coffin"></span><a to="/search#mortality">${feature.properties.species.vernacular_name}</a></h2>
    <i>${feature.properties.species.scientific_name}</i>
   <p><strong>Date</strong>&nbsp;:&nbsp;${feature.properties.date}<br>
      <strong>Cause</strong>&nbsp;:&nbsp;${feature.properties.death_cause.label}
    </dl>
    </p>`
  )
  // remove pm from layer to prevent action from geoman (no more drag/edit/remove ...)
  // console.log('layer', layer)
  // delete layer.pm
  // layer.setStyle({ pmIgnore: false })
}


const infrastructureGeoJsonOptions : GeoJSONOptions = reactive({
  onEachFeature : infrastructureOnEachFeature,
})


// const selectedFeatureGeoJsonOptions : GeoJSONOptions = reactive({})


const deathCasesGeoJsonOptions : GeoJSONOptions = reactive({
  onEachFeature: mortalityOnEachFeature ,
})

watch(mapObject, (newVal, oldVal) => {
  console.log('mapObject watcher', mapObject.value.getBounds())
})
watch(selectedFeature, (newVal, oldVal) => {

  if (JSON.stringify(newVal) !== JSON.stringify(oldVal)) {
    
    const newObj = leaflet.geoJSON(newVal)
    coordinatesStore.setCenter(newObj.getBounds().getCenter())
    coordinatesStore.setZoom(15)

  }
})

const getMapBounds = () => {
  console.log(mapObject.value.getBounds().toBBoxString())
  coordinatesStore.setMapBounds(mapObject.value.getBounds().toBBoxString())
  coordinatesStore.setZoom(mapObject.value.getZoom())
}

const hookUpDraw = async () => {
  mapObject.value = map.value?.leafletObject;
  console.log('mapObject.value', mapObject.value.getBounds(), map)
  mapReady.value = true;
  leaflet.control.locate({icon: 'mdi mdi-crosshairs-gps'}).addTo(mapObject.value)
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
    });
    mapObject.value.pm.setPathOptions({
          color: 'red',
          fillColor: 'red',
          fillOpacity: 0.4,
        })
    mapObject.value.on('pm:create', (e) => {
          createLayer.value = e.layer
          switch (mode) {
            case 'point':
              console.log('createLayer', createLayer.value.toGeoJSON())
              if (createLayer.value.toGeoJSON()) {
              coordinatesStore.setNewGeoJSONPoint(
                createLayer.value.toGeoJSON().geometry
              )
              mapObject.value?.pm.disableDraw()
              mapObject.value?.pm.addControls({
                drawMarker: false,
                dragMode: true,
                removalMode: true,
              })}
              break
            case 'line':
              coordinatesStore.newLineCoord = createLayer.value.toGeoJSON().geometry.coordinates
              mapObject.value?.pm.addControls({
                drawPolyline: false,
                editMode: true,
                removalMode: true,
              })
              break
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
  }
};

const levelColor = (feature) => {
  const levelNotes = {'RISK_L':1,'RISK_M':2,'RISK_H':3}
  const attractivity = feature.properties?.actions_infrastructure[0].pole_attractivity.code
  const dangerousness = feature.properties?.actions_infrastructure[0].pole_dangerousness.code
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



onBeforeMount(async () => {
  // const { circleMarker } = await import("leaflet/dist/leaflet-src.esm");
  infrastructureGeoJsonOptions.pointToLayer = (feature: Feature, latlng : any ) => {
    return leaflet.circleMarker(latlng, {
      radius: 5,
      fillColor: levelColor(feature),
      color: '#000',
      weight: 1,
      opacity: 1,
      fillOpacity: 0.8,
      // draggable: true,
    })
  }

  deathCasesGeoJsonOptions.pointToLayer = (feature: Feature, latlng : any ) => {
    const iconDict = {
      COD_EL: 'lightning-bolt',
      COD_IM : 'star'
    }
    const icon = iconDict[feature.properties?.death_cause?.code] || 'help';
    let deathCaseIcon = leaflet.divIcon({
      html: `<span class="mdi mdi-${icon}"></span>`,
      iconSize: [15, 15],
      className: 'mapMarkerIcon'}
      );
    return leaflet.marker(latlng, {icon: deathCaseIcon});

      // draggable: true,
    }
})



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

.leaflet-demo-control {
  background: lightgoldenrodyellow;
  border: 2px solid orange;
  border-radius:2px;
  padding: 10px;
  font-size: large;
  line-height: 30px;

}
</style>
