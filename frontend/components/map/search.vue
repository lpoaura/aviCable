<template>
  <l-map id="map" ref="map" class="d-flex" :zoom="zoom" :center="center" @ready="hookUpDraw" @zoom="getBbox"
    @moveend="getBbox">

    <!-- <l-map id="map" ref="map" class="d-flex align-stretch" :zoom="zoom" :center="center" @ready="hookUpDraw"> -->
    <template v-if="mapReady">
      <l-tile-layer v-for="baseLayer in baseLayers" :key="baseLayer.id" :name="baseLayer.name" :url="baseLayer.url"
        :visible="baseLayer.default" :attribution="baseLayer.attribution" :layer-type="baseLayer.layer_type" />
      <l-geo-json v-if="isFeatureCollection(lineStringData)" name="Lignes" layer-type="overlay"
        :geojson="lineStringData" :options="infrastructureGeoJsonOptions" :options-style="infrastructureLineStyle" />
      <l-geo-json v-if="isFeatureCollection(pointData)" name="Supports" layer-type="overlay" :geojson="pointData"
        :options="infrastructureGeoJsonOptions" />
      <l-geo-json v-if="isFeatureCollection(mortalityData)" name="Mortalité" layer-type="overlay"
        :geojson="mortalityData" :options="deathCasesGeoJsonOptions" />
      <l-geo-json v-if="bufferedSelectedFeature" :geojson="bufferedSelectedFeature"
        :options-style="selectedFeatureGeoJsonStyle" />
      <l-geo-json v-if="isFeatureCollection(operatedLineStringData)" name="Lignes neutralisées" layer-type="overlay"
        :geojson="operatedLineStringData" :options-style="infrastructureOperatedLineStyle" />
      <l-geo-json v-if="isFeatureCollection(operatedPointData)" name="Supports neutralisés" layer-type="overlay"
        :geojson="operatedPointData" :options="operatedInfrastructureGeoJsonOptions" />
      <!-- <l-geo-json v-if="newGeoJSONObject" :geojson="newGeoJSONObject" /> -->
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
import { storeToRefs } from 'pinia';
import "leaflet.locatecontrol"
import 'leaflet.locatecontrol/dist/L.Control.Locate.min.css'
// import 'leaflet-search'
import { OpenStreetMapProvider, GeoSearchControl } from "leaflet-geosearch"
import "leaflet-geosearch/assets/css/leaflet.css"
import { LMap, LTileLayer, LGeoJson, LControlLayers, LControl, LControlScale, LWmsTileLayer } from "@vue-leaflet/vue-leaflet";
// import { useMapLayersStore } from "store/mapLayersStore";
import buffer from '@turf/buffer'
import type { GeoJSON, Feature, FeatureCollection } from "geojson"
// import { useCablesStore } from "~/store/cablesStore"
import type { StoreGeneric } from "pinia"
import type {PointTuple, GeoJSONOptions, Layer, LatLng} from "leaflet";

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
const opLineRef : Ref<typeof LGeoJson | null> = ref(null)
const router = useRouter()
// Stores
const cableStore : StoreGeneric  = useCablesStore()
const mortalityStore: StoreGeneric = useMortalityStore()
const mapLayersStore : StoreGeneric = useMapLayersStore()
const coordinatesStore : StoreGeneric = useCoordinatesStore()


// Store values
const {zoom, center, bbox, selectedFeature, newGeoJSONObject} = storeToRefs(coordinatesStore)
const {
  infstrData,
  infstrDataLoadingStatus,
  pointData,
  operatedPointData,
  lineStringData,
  operatedLineStringData
} = storeToRefs(cableStore)
const {mortalityData} = storeToRefs(mortalityStore)
const {baseLayers} = storeToRefs(mapLayersStore)
  // const baseLayers = computed(() => mapLayersStore.baseLayers)
// const storedSelectedFeature: ComputedRef<Feature|null> =  computed<Feature|null>(() =>  coordinatesStore.selectedFeature)
const bufferedSelectedFeature : Ref<Feature|null> = ref(null)

const levelNotes : {[key: string]: number} = {'RISK_L':1,'RISK_M':2,'RISK_H':3}

watch(selectedFeature, (newVal, _oldVal) => {
  bufferedSelectedFeature.value = newVal  ? buffer(newVal, 150, {units: 'meters'}) : null
})

const infrastructurePopupContent = (feature) => `<h2><span class="mdi ${feature.geometry.type === 'Point' ? 'mdi-transmission-tower':'mdi-cable-data'}">
      </span><span id="routerLink" style="cursor: pointer">${feature.geometry.type === 'Point' ? 'Poteau':'Tronçon'}
        ${feature.properties?.owner.label} ${feature.properties?.id}</span></h2>`

const  isFeatureCollection = (obj: any): obj is FeatureCollection => {
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


const infrastructureOnEachFeature = (feature : Feature, layer : Layer) => {
  // layer.bindPopup(infrastructurePopupContent(feature))
  layer.on('click', ()=> {return selectedFeature.value = feature})
    // layer.on('popupopen', () => {
    //   const id = feature?.properties?.id
    //     const link = document.getElementById('routerLink');
    //     link.addEventListener('click', (event) => {
    //       event.preventDefault(); // Prevent the default anchor behavior
    //       if (['Point','Line'].includes(feature?.resourcetype) && id) {
    //         router.push(`/infrastructures/${id}`)
    //       }
    //     });
    //   });
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
    layer.on('click', (e)=> {console.debug('click', feature, e)})
  }
  // remove pm from layer to prevent action from geoman (no more drag/edit/remove ...)
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

watch(selectedFeature, (newVal, oldVal) => {
  if (JSON.stringify(newVal) !== JSON.stringify(oldVal)) {
    const newObj = leaflet.geoJSON(newVal)
    mapObject.value?.setView(newObj.getBounds().getCenter(), 15)
  }
})

watch(createLayer, (newLayer, _oldLayer) => {
  if (newLayer && newLayer.toGeoJSON()) {
    // You can perform additional actions here based on the unique layer's changes
    newGeoJSONObject.value = newLayer.toGeoJSON()
  } else {
    console.debug('Unique layer removed');
  }
});

const getBbox = () => {
  if (mapObject.value) {
    zoom.value = mapObject.value.getZoom()
    center.value = mapObject.value.getCenter()
    bbox.value = mapObject.value.getBounds().toBBoxString()
  }
}



const selectedFeatureGeoJsonStyle = (_feature: Feature) => {
  const color='#03A9F4' // blue-lighten
    return {
      color: color,
      fillColor: color,
      weight: 2,
      opacity: 0.5,
    }
  }

  const infrastructureLineStyle = (feature: Feature) => {
    return  {
      color:  lineColor(feature),
      weight: 5,
      // draggable: true,
    }
  }
  const infrastructureOperatedLineStyle = (_feature: Feature) => {
    return  {
      color:  '#00ff00',
      weight: 2,
      // draggable: true,
    }
  }
const hookUpDraw = async () => {
  console.log(map.value)
  mapObject.value = map.value?.leafletObject;

  if (mapObject.value) {
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
            color: '#ba02f2',
            fillColor: '#ba02f2',
            fillOpacity: 0.4,
          })
      mapObject.value.on('pm:create', (e) => {
        if (createLayer.value) {
          mapObject.value.removeLayer(createLayer.value);
        }
            createLayer.value = e.layer
            if (createLayer.value){
              // if (createLayer.value.toGeoJSON()) {
              //   coordinatesStore.setNewGeoJSONObject(
              //     createLayer.value.toGeoJSON().geometry
              //   )
              // }
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
            )
            // // set listener on drag event on this layer
            // this.handleDrag(createLayer)

            // // in case of remove event, trigger handleRemove() method
            // e.layer.on('pm:remove', (_e) => {
            //   this.handleRemove()
            // })

      // mapObject.value.on("pm:drawstart", ({ workingLayer, shape }) => {
      //   workingLayer.on("pm:vertexadded", (e) => {
      //     geofence.value.push(e)
      //   });
      // });

      // mapObject.value.on("pm:drawend", () => {
      //   console.log("drawend", geofence.value);
      // });
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

const lineColor=(feature:Feature) => {
  const lastDiag=feature.properties?.diagnosis[0]
  if (lastDiag) {
    const sgmt_moving_risk = lastDiag.sgmt_moving_risk?.code
    const sgmt_landscape_integr_risk = lastDiag.sgmt_landscape_integr_risk?.code
    const sgmt_topo_integr_risk = lastDiag.sgmt_topo_integr_risk?.code
    const note = levelNotes[sgmt_moving_risk] + levelNotes[sgmt_landscape_integr_risk] + levelNotes[sgmt_topo_integr_risk]
    if (note < 4) {
      return 'blue'
    }
    if (note >= 4 && note < 7)
    {
      return 'orange'
    }
    else {return 'red'}
  }
  return 'grey'
}

const supportColor = (feature: Feature) => {
  const lastDiag=feature.properties?.diagnosis[0]
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

watch(bbox, (newVal, _oldVal) => {
  cableStore.cancelRequest();
  mortalityStore.cancelRequest();

  if (zoom.value >= 10) {
    cableStore.getInfstrData({in_bbox: newVal})
    cableStore.getOpData({in_bbox: newVal})
    mortalityStore.getMortalityData({in_bbox: newVal})
  } else {
    infstrDataLoadingStatus.value = false
    infstrData.value = {}
    mortalityData.value= {} as FeatureCollection
  }
})

onBeforeMount(async () => {
  // const { circleMarker } = await import("leaflet/dist/leaflet-src.esm");
  infrastructureGeoJsonOptions.pointToLayer = (feature: Feature, latlng : LatLng | null ) => {
    if (latlng) {
      return leaflet.circleMarker(latlng, {
        radius: 6,
        fillColor: supportColor(feature),
        color: '#000',
        weight: 0.5,
        opacity: 0.5,
        fillOpacity: 0.8,
        // draggable: true,
      })
    }
  }

  operatedInfrastructureGeoJsonOptions.pointToLayer = (_feature: Feature, latlng : LatLng | null ) => {
    if (latlng) {
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
  }

  selectedFeatureGeoJsonOptions.pointToLayer = (feature: Feature, latlng : LatLng | null ) => {
    if (feature.resourcetype === 'Point' && latlng) {
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

  deathCasesGeoJsonOptions.pointToLayer = (feature: Feature, latlng : LatLng ) => {
    console.log('deathCasesGeoJsonOptions', feature, latlng)
      if(latlng){
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
      }
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
</style>
