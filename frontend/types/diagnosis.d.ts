declare interface DiagData {
  date: string;
  remark: string | null;
  infrastructure: number | null;
  pole_type_id: Array<number>;
  pole_type: Array<Object>,
  neutralized: boolean;
  condition_id: number | null;
  condition: Object;
  attraction_advice: boolean;
  dissuasion_advice: boolean;
  isolation_advice: boolean;
  pole_attractivity_id: number | null;
  condition: Object | null;
  pole_dangerousness_id: number | null;
  ole_dangerousness: Object | null;
  media_id?: Array<number>;
  change_advice: boolean;
  technical_proposal: string  | null;
}

declare interface Diagnosis {
  id: number;
  infrastructure: number;
  date: string;
  remark: string;
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
