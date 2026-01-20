import type { Geometry, Feature, FeatureCollection } from "geojson";
import type {Nomenclature} from "./nomenclature"

export type GeoArea = {
  code: string;
  id: number;
  name: string;
  type: Nomenclature | number;
};

export type GeoAreaFeature = Feature<Geometry, GeoArea>;

export type GeoAreaFeatureCollection = FeatureCollection<Geometry, GeoArea>;

export type GeoAreasFetchParams = {
    in_bbox?: string;
    type__code?: string;
}