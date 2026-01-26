/**
 * Nuxt Point module: coordinatesStore to handle creation of new Point
 */

import { defineStore } from "pinia";
import type { LineString, Feature } from "geojson";
import type { LatLng } from "leaflet";
import type { CablesFeature } from "~/types/cables";

interface NewPointCoord {
  lat: number | null;
  lng: number | null;
  default?: null;
}

export const useCoordinatesStore = defineStore("coordinates", {
  state: () => ({
    selectedFeature: null as Feature | null,
    center: { lat: 46.64, lng: 2.2 } as LatLng,
    zoom: 6,
    newPointCoord: {} as NewPointCoord,
    newLineCoord: [],
    newGeoJSONLine: { coordinates: [], type: "LineString" } as LineString,
    newGeoJSONObject: {} as Feature,
    bbox: null as string | null,
    mortalityGetInfrastructure: false,
    mortalityInfrastructure: {} as CablesFeature | null,
  }),
  getters: {
    /**
     * Getter for newPointCoord state values
     *
     * @param {state} state of this store module
     * @return {JSON object} object with latitude and longitude data
     */
    getNewPointCoord(state) {
      return state.newPointCoord;
    },
    /**
     * Getter for newLineCoord state values
     *
     * @param {state} state of this store module
     * @return {JSON object} object with Line coordinates data (latitude and longitude)
     */
    getNewLineCoord(state) {
      return state.newLineCoord;
    },
    getNewGeoJSONObject(state) {
      return state.newGeoJSONObject;
    },
  },
  actions: {
    setbbox(data: string) {
      this.bbox = data;
    },
    setSelectedFeature(data: Feature) {
      console.debug("setSelectedFeature", data)
      this.selectedFeature = data;
    },
    setCenter(data: LatLng) {
      this.center = data;
    },
    setZoom(data: number) {
      this.zoom = data;
    },
    setNewPointCoord(data: NewPointCoord) {
      this.newPointCoord = data;
    },
    setNewLineCoord(data: []) {
      this.newLineCoord = data;
    },
    setNewGeoJSONObject(data: Feature) {
      this.newGeoJSONObject = data;
    },
    setNewGeoJSONLine(data: LineString) {
      this.newGeoJSONLine = data;
    },
  },
});
