import type { Geometry } from "geojson";

export interface Media  {
  author?: string | null;
  date: string;
  id: number;
  remark?: string | null;
  source?: string | null;
  storage: any;
}

export type Diagnosis = {
  attractionAdvice?: boolean
  changeAdvice?: boolean
  condition: Nomenclature
  conditionId?: any | null
  date?: string
  dissuasionAdvice?: boolean
  id: number
  infrastructure: any
  isolationAdvice?: boolean
  last?: boolean
  media: Media[]
  mediaId?: any
  neutralized?: boolean
  poleAttractivity: Nomenclature
  poleAttractivityId?: any | null
  poleDangerousness: Nomenclature
  poleDangerousnessId?: any | null
  poleType: Nomenclature[]
  poleTypeId?: any
  remark?: string | null
  sgmtBuildIntegrRisk: Nomenclature
  sgmtBuildIntegrRiskId?: any | null
  sgmtMovingRisk: Nomenclature
  sgmtMovingRiskId?: any | null
  sgmtTopoIntegrRisk: Nomenclature
  sgmtTopoIntegrRiskId?: any | null
  sgmtVegetIntegrRisk: Nomenclature
  sgmtVegetIntegrRiskId?: any | null
  technicalProposal?: string | null
}

export type InfrastructurePolymorphic = {
  createdBy: any | null
  geoArea?: any
  id: number
  owner: any
  polymorphicCtype: any | null
  sensitiveArea?: any
  timestampCreate: string
  timestampUpdate: string
  updatedBy: any | null
  uuid: string
}

export type GeoArea = {
  code: string
  id: number
  name: string
  type: Nomenclature
}

export interface Equipment {
  comment: string | null
  count: number
  reference: string | null
  type?: Nomenclature[]
  type_id?: number
}

export type Operation = {
  date?: string
  equipments: Equipment[]
  id: number
  infrastructure: number
  last?: boolean
  media: Media[]
  mediaId?: number[]
  remark?: string | null
}

export type SensitiveArea = {
  code: string
  id: number
  name: string
}

export type Line = {
  diagnosis: Diagnosis[]
  geoArea: GeoArea[]
  geom?: Geometry | null
  id: number
  operations: Operation[]
  owner: Nomenclature
  ownerId: any
  sensitiveArea: SensitiveArea[]
}

export type OperationPolymorphic = {
  createdBy: any | null
  date?: string
  equipments?: any
  id: number
  infrastructure: any
  last?: boolean
  media?: any
  polymorphicCtype: any | null
  remark?: string | null
  timestampCreate: string
  timestampUpdate: string
  updatedBy: any | null
  uuid: string
}

export type Point = {
  diagnosis: Diagnosis[]
  geoArea: GeoArea[]
  geom: any
  id: number
  operations: Operation[]
  owner: Nomenclature
  ownerId: any
  sensitiveArea: SensitiveArea[]
}

