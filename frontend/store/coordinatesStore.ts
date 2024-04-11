/**
 * Nuxt Point module: coordinatesStore to handle creation of new Point
 */

import { defineStore } from "pinia";
import type { Point, LineString, Feature } from "geojson";
import type { PointTuple } from "leaflet";

interface NewPointCoord {
  lat: number | null;
  lng: number | null;
  default?: null;
}

export const useCoordinatesStore = defineStore("coordinates", {
  state: () => ({
    selectedFeature: {} as Feature,
    center: [46.6423682169416, 2.1940236627886227] as PointTuple,
    zoom: 6,
    newPointCoord: {} as NewPointCoord,
    newLineCoord: [],
    newGeoJSONPoint: { coordinates: [], type: "Point" } as Point,
    newGeoJSONLine: { coordinates: [], type: "LineString" } as LineString,
    mapBounds: null as string|null,
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
  },
  actions: {
    setMapBounds(data: string) {
      this.mapBounds = data;
    },
    setSelectedFeature(data: Feature) {
      console.log('selectedFeature', data)
      this.selectedFeature = data;
    },
    setCenter(data: PointTuple) {
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
    setNewGeoJSONPoint(data: Point) {
      this.newGeoJSONPoint = data;
    },
    setNewGeoJSONLine(data: LineString) {
      this.newGeoJSONLine = data;
    },
  },
});
