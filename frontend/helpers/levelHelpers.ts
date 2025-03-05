import type { Risk } from "~/types/diagnosis";

export const notationValues: (
  item: any,
  t: (key: string) => string,
  detail: bool
) => Risk = (item, t, detail = false) => {
  const risks = {
    NE: { note: 0, color: "grey", label: t(detail ? 'notEvaluated' : 'ne') },
    RISK_L: { note: 1, color: "blue", label: t(detail ? "lowRisk" : "low") },
    RISK_M: { note: 2, color: "orange", label: t(detail ? "midRisk" : "mid") },
    RISK_H: {
      note: 3,
      color: "red lighten-1 white--text",
      label: t(detail ? "highRisk" : "high"),
    },
  };
  const diagnosis = item.properties.diagnosis[0];
  let result = "NE";
  if (diagnosis) {
    if (item.resourcetype == "Point") {
      const note =
        risks[diagnosis.pole_attractivity?.code]?.note +
        risks[diagnosis.pole_dangerousness?.code]?.note;
      result = note < 3 ? "RISK_L" : note >= 5 ? "RISK_H" : "RISK_M";
    } else if (item.resourcetype == "Line") {
      // TODO: Manage lines risks
      const note =
        risks[diagnosis.sgmt_landscape_integr_risk?.code]?.note +
        risks[diagnosis.sgmt_moving_risk?.code]?.note +
        risks[diagnosis.sgmt_topo_integr_risk?.code]?.note;
      result = note < 4 ? "RISK_L" : note >= 7 ? "RISK_H" : "RISK_M";
    }
  }
  return risks[result];
};
