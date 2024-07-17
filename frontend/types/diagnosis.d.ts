export interface DiagData {
  id?: number|null;
  date: string|Date;
  remark: string | null;
  technical_proposal: string|null;
  infrastructure: number | null;
  pole_type_id: Array<number>;
  neutralized: boolean;
  condition_id: number | null;
  attraction_advice: boolean;
  dissuasion_advice: boolean;
  isolation_advice: boolean;
  pole_attractivity_id: number | null;
  pole_dangerousness_id: number | null;
  media_id: Array<number>;
}

export interface Diagnosis {
  id?: number|null;
  infrastructure: number;
  date: string;
  remark: string|null;
  technical_proposal: string|null;
  neutralized: boolean;
  condition: number;
  isolation_advice: boolean;
  dissuasion_advice: boolean;
  attraction_advice: boolean;
  pole_type: Array<NomenclatureItem>;
  pole_attractivity: NomenclatureItem;
  pole_dangerousness: Array<NomenclatureItem>;
  sgmt_build_integr_risk: number;
  sgmt_moving_risk: number;
  sgmt_topo_integr_risk: number;
  sgmt_veget_integr_risk: number;
  media: Array<T>;
  last?: boolean;
}
