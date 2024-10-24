import type { Geometry } from "geojson";

export interface Media {
  author?: string | null;
  date: string;
  id: number;
  remark?: string | null;
  source?: string | null;
  storage: string | null;
}

export type Diagnosis = {
  attractionAdvice?: boolean;
  changeAdvice?: boolean;
  condition: Nomenclature;
  conditionId?: any | null;
  date?: string;
  dissuasionAdvice?: boolean;
  id: number;
  infrastructure?: number;
  isolationAdvice?: boolean;
  last?: boolean;
  media: Media[];
  mediaId?: number;
  neutralized?: boolean;
  poleAttractivity: Nomenclature;
  poleAttractivityId?: number | null;
  poleDangerousness: Nomenclature;
  poleDangerousnessId?: number | null;
  poleType: Nomenclature[];
  poleTypeId?: number;
  remark?: string | null;
  sgmtBuildIntegrRisk: Nomenclature;
  sgmtBuildIntegrRiskId?: number | null;
  sgmtMovingRisk: Nomenclature;
  sgmtMovingRiskId?: number | null;
  sgmtTopoIntegrRisk: Nomenclature;
  sgmtTopoIntegrRiskId?: number | null;
  sgmtVegetIntegrRisk: Nomenclature;
  sgmtVegetIntegrRiskId?: number | null;
  technicalProposal?: string | null;
};

export type InfrastructurePolymorphic = {
  createdBy: any | null;
  geoArea?: any;
  id: number;
  owner: any;
  polymorphicCtype: any | null;
  sensitiveArea?: any;
  timestampCreate: string;
  timestampUpdate: string;
  updatedBy: any | null;
  uuid: string;
};

export type GeoArea = {
  code: string;
  id: number;
  name: string;
  type: Nomenclature;
};

export interface Equipment {
  comment: string | null;
  count: number;
  reference: string | null;
  type?: Nomenclature[];
  type_id?: number;
}

export type Operation = {
  date?: string;
  equipments: Equipment[];
  id: number;
  infrastructure: number;
  last?: boolean;
  media: Media[];
  mediaId?: number[];
  remark?: string | null;
};

export type SensitiveArea = {
  code: string;
  id: number;
  name: string;
};

export type Line = {
  diagnosis: Diagnosis[];
  geoArea: GeoArea[];
  geom?: Geometry | null;
  id: number;
  operations: Operation[];
  owner: Nomenclature;
  ownerId: any;
  sensitiveArea: SensitiveArea[];
};

export type OperationPolymorphic = {
  createdBy: any | null;
  date?: string;
  equipments?: any;
  id: number;
  infrastructure: any;
  last?: boolean;
  media?: any;
  polymorphicCtype: any | null;
  remark?: string | null;
  timestampCreate: string;
  timestampUpdate: string;
  updatedBy: any | null;
  uuid: string;
};

export type Point = {
  diagnosis: Diagnosis[];
  geoArea: GeoArea[];
  geom?: Geometry | null;
  id: number;
  operations: Operation[];
  owner: Nomenclature;
  ownerId: any;
  sensitiveArea: SensitiveArea[];
};

export type Infrastructure = {
  diagnosis: Diagnosis[];
  geoArea: GeoArea[];
  geom?: Geometry | null;
  id: number;
  operations: Operation[];
  owner: Nomenclature;
  ownerId: any;
  sensitiveArea: SensitiveArea[];
};

export interface CablesFeature extends Feature {
  properties?: {
      resourcetype?: string; // Optional key for resource type
      [key: string]: any; // Allow other properties
  };
}

export type CablesFeatureCollection = FeatureCollection<CablesFeature>;
