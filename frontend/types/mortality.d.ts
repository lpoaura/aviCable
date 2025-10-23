import type { Geometry, Feature, GeoJsonProperties, FeatureCollection } from "geojson";
import type { Nomenclature } from "./nomenclature";
import type { Medias } from "./media"
import type { UserSimple } from "./user"
import type { Infrastructure } from "./cables";
import type { GeoApiFrProvider } from "leaflet-geosearch";


export interface MortalityStoreState {
  mortalityData: FeatureCollection; // Replace 'any' with a more specific type if possible
  mortalityItem: Feature;
  error: Error | null;
  controller: AbortController | null;
}

export interface MortalityData {
  properties: {
    id: number;
    vernacular_name: string;
    scientific_name: string;
    death_cause?: string;
    default: boolean | undefined;
  };
}

export interface Species {
    id:number;
    code?: string;
    scientific_name: string;
    vernacular_name: string;
    active?: boolean;
    photo?: string;
}

interface MortalityInfrastructure {
    id: number;
    network_type: Nomenclature;
}

export interface Mortality extends GeoJsonProperties {
    id?: number;
    date?: string | Date;
    species?: Species | number;
    species_id?: number;
    death_cause: Nomenclature | number;
    infrstr: MortalityInfrastructure | number ;
    infrstr_id?: number;
    nb_death: number;
    author: string | null;
    data_source: string | null;
    data_source_url: string | null;
    comment: string | null;
    media_id?: number[];
    media?: Media[];
    areas?: GeoArea[];
    resourcetype?: string | null;
    created_by?: UserSimple;
    updated_by?: UserSimple;
    timestamp_create?: string;
    timestamp_update?: string;
    geom: Geometry | null;
};



export interface MortalityFeature extends Feature<Geometry, Mortality> {
    id: number;
    properties: Mortality;
}
