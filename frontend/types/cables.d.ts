import type { Geometry, Feature, GeoJsonProperties, FeatureCollection } from "geojson";
import type {Polyline, Marker} from "leaflet"
import type { Nomenclature } from "./nomenclature";
import type { Medias } from "./media"
import type { UserSimple } from "./user"

export type NewLayerType = Polyline | Marker

export interface DiagData {
  id?: number | null;
  date?: string | Date;
  remark: string | null;
  technical_proposal: string | null;
  change_advice: boolean;
  infrastructure: number | null;
  arming_id: Array<number>;
  neutralized: boolean;
  condition_id: number | null;
  attraction_advice: boolean;
  dissuasion_advice: boolean;
  isolation_advice: boolean;
  pole_attractivity_id?: number | null;
  pole_dangerousness_id?: number | null;
  sgmt_moving_risk_id?: number | null;
  sgmt_topo_integr_risk_id?: number | null;
  sgmt_landscape_integr_risk_id?: number | null;
  media_id?: Array<number>;
}

export type Diagnosis = DiagData & {
  change_advice?: boolean;
  infrastructure?: number;
  last?: boolean;
  media: Medias;
  condition: Nomenclature;
  pole_attractivity: Nomenclature;
  pole_dangerousness: Nomenclature;
  arming: Nomenclature[];
  sgmt_build_integr_risk: Nomenclature;
  sgmt_moving_risk: Nomenclature;
  sgmt_topo_integr_risk: Nomenclature;
  sgmt_veget_integr_risk: Nomenclature;
  sgmt_landscape_integr_risk: Nomenclature;
  created_by: UserSimple;
  updated_by: UserSimple;
  timestamp_create: string;
  timestamp_update: string;
};

export type InfrastructurePolymorphic = {
  created_by: any | null;
  geo_area?: any;
  id: number;
  network_type: any;
  polymorphic_ctype: any | null;
  sensitive_area?: any;
  timestamp_create: string;
  timestamp_update: string;
  updated_by: any | null;
  uuid: string;
};

export type GeoArea = {
  code: string;
  id: number;
  name: string;
  type: Nomenclature;
};

export interface Equipment {
  id?: number;
  comment: string | null;
  count: number;
  reference: string | null;
  type?: Nomenclature;
  type_id?: number | null;
}

export interface OperationData {
  id?: number | null;
  date?: string | Date;
  neutralization_level: string;
  equipments: Equipment[];
  infrastructure: number;
  last?: boolean;
  media_id?: number[];
  remark?: string | null;
  geom?: Geometry | null;
  resourcetype?: string | null;
}

export interface Operation extends GeoJsonProperties {
  date?: string | Date;
  neutralization_level: string;
  equipments: Equipment[];
  id?: number;
  infrastructure: number;
  last?: boolean;
  media: Medias | number[];
  media_id?: number[];
  remark?: string | null;
  geom?: Geometry | null;
  resourcetype?: string | null;
};



interface OperationFeature extends Feature<Geometry, Operation> {
  resourcetype: string;
  properties: Operation;
}

interface OperationFeatureCollection extends FeatureCollection {
  features: OperationFeature[];
}

export type SensitiveArea = {
  code: string;
  id: number;
  name: string;
};

export type Line = {
  diagnosis: Diagnosis[];
  geo_area: GeoArea[];
  geom?: Geometry | null;
  id: number;
  operations: Operation[];
  network_type: Nomenclature;
  network_type_id: any;
  sensitive_area: SensitiveArea[];
};

export type OperationPolymorphic = {
  created_by: any | null;
  date?: string;
  equipments?: any;
  id: number;
  infrastructure: any;
  last?: boolean;
  media?: any;
  polymorphic_ctype: any | null;
  remark?: string | null;
  timestamp_create: string;
  timestamp_update: string;
  updated_by: any | null;
  uuid: string;
};

export type Point = {
  diagnosis: Diagnosis[];
  geo_area: GeoArea[];
  geom?: Geometry | null;
  id: number;
  operations: Operation[];
  network_type: Nomenclature;
  network_type_id: any;
  sensitive_area: SensitiveArea[];
};

export type Infrastructure = {
  diagnosis: Diagnosis[];
  geo_area: GeoArea[];
  geom?: Geometry | null;
  id: number;
  operations: Operation[];
  network_type: Nomenclature;
  network_type_id: number;
  sensitive_area: SensitiveArea[];
};

export interface CablesFeature extends Feature {
  properties?: {
    resourcetype?: string; // Optional key for resource type
    [key: string]: any; // Allow other properties
  };
  resourcetype?: string;
}

export type CablesFeatureCollection = FeatureCollection<CablesFeature>;

export interface Risk {
  note: number;
  label: string;
  color: string;
}

export interface NetworkFeature extends Feature {
  properties: {
    type?: string;
    category?: string;
    [key: string]: any; 
  };
}

// export interface NetworkFeature extends Feature {
//   properties: {
//     type?: string;
//     category?: string; 
//     [key: string]: any; 
//   } | never; // Ensures properties is never null
// }


export interface NetworkProperties extends GeoJsonProperties {
    type?: string;
    category?: string; 
};



interface NetworkFeature extends Feature<Geometry, NetworkProperties> {
  properties: Operation;
}


export type NetworkFeatureCollection = FeatureCollection<NetworkFeature>;
