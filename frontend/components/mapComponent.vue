<template>
  <l-map
    ref="map" class="d-flex align-stretch" :class="editMode ? 'change-map' : 'view-map'" :center="center"
    :bounds="bounds" :max-bounds="maxBounds" @ready="onMapReady()">
    <l-control-layers position="topright"></l-control-layers>
    <l-tile-layer
      v-for="baseLayer in baseLayers" :key="baseLayer.id" :name="baseLayer.name" :url="baseLayer.url"
      :visible="baseLayer.default" :attribution="baseLayer.attribution" layer-type="base" />
    <!-- Display of existing Point layer-->
    <l-geo-json
      v-if="pointData" name="pointData" :geojson="pointData" :options-style="styleData"
      :options="GeojsonOptions" />
    <l-geo-json
      v-if="cablesData" name="lineStringData" :geojson="lineStringData" :options-style="styleData"
      :options="GeojsonOptions" />
    
    <!-- <l-icon-default :image-path="path" /> -->
  </l-map>
</template>

<script>
import { latLngBounds } from 'leaflet'
import { mapGetters } from 'vuex'
import '@geoman-io/leaflet-geoman-free'
import '@geoman-io/leaflet-geoman-free/dist/leaflet-geoman.css'

export default {
  name: 'DataMap',
  props: { editMode: Boolean, mode: { type: String, default: null } },

  data() {
    return {
      newLineMarkers: [[45, 7]],
      map: null,
      // creation markers layer
      createLayer: null,
      // Map parameters
      bounds: latLngBounds([
        [40, -6],
        [52, 10],
      ]),
      maxBounds: latLngBounds([
        [40, -6],
        [52, 10],
      ]),
      zoom: 5,
      path: '/images/',
      center: [47.41322, -1.219482],
    }
  },

  computed: {
    // Map property options to matching function
    GeojsonOptions() {
      return {
        onEachFeature: this.GeoJsonOnEachFeature,
        pointToLayer: this.GeoJsonPointToLayer,
      }
    },
    /**
     * GeoJsonOnEachFeature(): Method that defines code executed for each Feature
     */
    GeoJsonOnEachFeature() {
      return (feature, layer) => {
        // TODO To be adapted
        layer.bindPopup(
          `ma <strong>bindPopup</strong> pour<br>${feature.geometry.type} avec  id =>${feature.properties.id}`
        )
        // remove pm from layer to prevent action from geoman (no more drag/edit/remove ...)
        delete layer.pm
        layer.setStyle({ pmIgnore: false })
      }
    },
    ...mapGetters({
      cablesData: 'cablesStore/infstrDataFeatures',
      pointData: 'cablesStore/pointDataFeatures',
      lineStringData: 'cablesStore/lineDataFeatures',
      newPointCoord: 'coordinatesStore/newPointCoord',
      newLineCoord: 'coordinatesStore/newLineCoord',
      baseLayers: 'mapLayersStore/baseLayers',
    }),
  },

  watch: {
    /**
     * Watcher for "newPointCoord" value
     *
     * Only activated on "editMode=true" with "mode='point'" and if coordinate data are well
     * defined.
     * Marker position is changed based on new coordinate value.
     * If Marker does not exist, it is created with new value.
     * Map is centered on the new point.
     */
    newPointCoord(newVal) {
      if (this.editMode && this.mode === 'point') {
        if (this.createLayer) {
          if (newVal && newVal.lat !== null && newVal.lng !== null) {
            this.createLayer.setLatLng(new L.LatLng(newVal.lat, newVal.lng))
          } else {
            this.createLayer.remove()
            this.createLayer = null
          }
        } else if (newVal && newVal.lat !== null && newVal.lng !== null) {
          this.map = this.$refs.map.mapObject
          this.map.on('layeradd', (e) => {
            this.createLayer = e.layer
            this.map.pm.addControls({
              drawMarker: false,
              dragMode: true,
              removalMode: true,
            })
          })
          // const layer = new L.Marker([newVal.lat, newVal.lng]).addTo(this.map)
          // set listener on drag event on this layer
          this.handleDrag(this.createLayer)
          // in case of remove event, tigger handleRemove() method
          this.createLayer.on('pm:remove', (_e) => this.handleRemove())
        }
      }
    },
  },
  methods: {
    /**
     * handleDrag(): Method that records new Point coordinates through "coordinatesStore" at the
     * end of drag event.
     *
     * @param {Object} layer the marker belong to.
     */
    handleDrag(layer) {
      layer.on('pm:dragend', (e) => {
        this.$store.commit('coordinatesStore/addPointCoord', {
          lng: e.layer.toGeoJSON().geometry.coordinates[0],
          lat: e.layer.toGeoJSON().geometry.coordinates[1],
        })
      })
    },
    /**
     * handleRemove(): Method that manages removing of new created layer removal. It refers to
     * layer "createLayer" defined in the current component.
     *
     * It re-initialize coordinates data through "coordinatesStore" and managed access to
     * appropriate controls, depending geometry type of the ongoing created marker.
     */
    handleRemove() {
      this.createLayer = null
      switch (this.mode) {
        case 'point':
          this.$store.commit('coordinatesStore/addPointCoord', {
            lat: null,
            lng: null,
          })
          this.map.pm.disableGlobalRemovalMode()
          this.map.pm.addControls({
            drawMarker: true,
            dragMode: false,
            removalMode: false,
          })
          break

        case 'line':
          this.$store.commit('coordinatesStore/addLineCoord', [])
          this.map.pm.addControls({
            drawPolyline: true,
            editMode: false,
            removalMode: false,
          })
          break
      }
    },
    // INFO: Passé en computed, onEachFeature devient alors un object
    // (j'avais un message comme quoi le props options attendait un objet et non une function)
    // C'est aussi le cas ici: https://vue2-leaflet.netlify.app/examples/geo-json.html
    // onEachFeature(_feature, layer) {
    //   layer.bindPopup('coucou', _feature)
    // },
    changePointMarker(_feature, latlng) {
      if (feature.geometry.type === 'Point') {
        return LCircleMarker(latlng, {
          radius: 2,
          fillOpacity: 0.85,
        })
      }
    },
    /**
     * GeoJsonPointToLayer(): Method that defines point appearance as point symbol instead of Maker
     * symbol
     */
    // TODO Style to be reviewed
    GeoJsonPointToLayer(_feature, latlng) {
      return L.circleMarker(latlng, {
        radius: 5,
        fillColor: '#ff7800',
        color: '#000',
        weight: 1,
        opacity: 1,
        fillOpacity: 0.8,
        draggable: true,
      })
    },
    /**
     * styleData(feature): Method() that define style of LGeoJson tags (cf. option-style property)
     *
     * @param {Feature} feature
     */
    styleData(feature) {
      if (feature.geometry.type === 'LineString') {
        return {
          color: 'green',
        }
      } else {
        return {
          color: 'red',
        }
      }
    },
    /**
     * onMapReady(): Method triggered whan LMap is ready.
     *
     * Actions on "pm" (for polygon management) property of map.
     * It adds and configures controls, options, and set listener on various events (create, drag,
     * remove)
     */
    onMapReady() {
      this.map = this.$refs.map.mapObject
      if (this.editMode) {
        this.map.pm.addControls({
          position: 'topleft',
          drawMarker: this.mode === 'point',
          drawCircleMarker: this.mode === 'circle-marker',
          drawPolyline: this.mode === 'line',
          drawPolygon: this.mode === 'polygon',
          drawRectangle: this.mode === 'rectangle',
          drawCircle: this.mode === 'circle',
          editMode: false,
          dragMode: false,
          removalMode: false,
          cutPolygon: false,
          rotateMode: false,
        })
        this.map.pm.setPathOptions({
          color: 'red',
          fillColor: 'red',
          fillOpacity: 0.4,
        })
        // Action on Point/Line creation
        this.map.on('pm:create', (e) => {
          this.createLayer = e.layer

          switch (this.mode) {
            case 'point':
              this.$store.commit('coordinatesStore/addPointCoord', {
                lng: e.layer.toGeoJSON().geometry.coordinates[0],
                lat: e.layer.toGeoJSON().geometry.coordinates[1],
              })
              this.map.pm.disableDraw()
              this.map.pm.addControls({
                drawMarker: false,
                dragMode: true,
                removalMode: true,
              })
              break
            case 'line':
              this.$store.commit(
                'coordinatesStore/addLineCoord',
                e.layer.toGeoJSON().geometry.coordinates
              )
              this.map.pm.addControls({
                drawPolyline: false,
                editMode: true,
                removalMode: true,
              })
              break
          }
          // set listener on drag event on this layer
          this.handleDrag(this.createLayer)

          // in case of remove event, trigger handleRemove() method
          e.layer.on('pm:remove', (_e) => {
            this.handleRemove()
          })
        })
      }
    },
  },
}
</script>

<style scoped>
.fab {
  z-index: 10000;
}

.view-map {
  cursor: grab;
}

.change-map {
  cursor: crosshair;
}
</style>
