export type MediaSerializer = {
  author?: string | null
  date: string
  id: number
  remark?: string | null
  source?: string | null
  storage: any
}

export type DiagnosisSerializer = {
  attractionAdvice?: boolean
  changeAdvice?: boolean
  condition: NomenclatureSerializer
  conditionId?: any | null
  date?: string
  dissuasionAdvice?: boolean
  id: number
  infrastructure: any
  isolationAdvice?: boolean
  last?: boolean
  media: MediaSerializer[]
  mediaId?: any
  neutralized?: boolean
  poleAttractivity: NomenclatureSerializer
  poleAttractivityId?: any | null
  poleDangerousness: NomenclatureSerializer
  poleDangerousnessId?: any | null
  poleType: NomenclatureSerializer[]
  poleTypeId?: any
  remark?: string | null
  sgmtBuildIntegrRisk: NomenclatureSerializer
  sgmtBuildIntegrRiskId?: any | null
  sgmtMovingRisk: NomenclatureSerializer
  sgmtMovingRiskId?: any | null
  sgmtTopoIntegrRisk: NomenclatureSerializer
  sgmtTopoIntegrRiskId?: any | null
  sgmtVegetIntegrRisk: NomenclatureSerializer
  sgmtVegetIntegrRiskId?: any | null
  technicalProposal?: string | null
}

export type InfrastructurePolymorphicSerializer = {
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

export type GeoAreaSerializer = {
  code: string
  id: number
  name: string
  type: NomenclatureSerializer
}

export type EquipmentSerializer = {
  comment?: string | null
  count?: number
  reference?: string | null
  type: NomenclatureSerializer[]
}

export type OperationSerializer = {
  date?: string
  equipments: EquipmentSerializer[]
  id: number
  infrastructure: any
  last?: boolean
  media: MediaSerializer[]
  mediaId?: any
  remark?: string | null
}

export type SensitiveAreaSerializer = {
  code: string
  id: number
  name: string
}

export type LineSerializer = {
  diagnosis: DiagnosisSerializer[]
  geoArea: GeoAreaSerializer[]
  geom?: any | null
  id: number
  operations: OperationSerializer[]
  owner: NomenclatureSerializer
  ownerId: any
  sensitiveArea: SensitiveAreaSerializer[]
}

export type OperationPolymorphicSerializer = {
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

export type PointSerializer = {
  diagnosis: DiagnosisSerializer[]
  geoArea: GeoAreaSerializer[]
  geom: any
  id: number
  operations: OperationSerializer[]
  owner: NomenclatureSerializer
  ownerId: any
  sensitiveArea: SensitiveAreaSerializer[]
}

