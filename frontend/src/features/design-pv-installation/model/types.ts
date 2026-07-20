export interface PvDesignFormValues {
  installation_area_m2: string;
  installation_power_kw: string;
  max_pln_budget: string;
  on_roof_installation: boolean;
  roof_angle: string;
  distance_from_inverter_to_modules_m: string;
  shading_likert: string;
}

export const INITIAL_PV_DESIGN_FORM_VALUES: PvDesignFormValues = {
  installation_area_m2: "",
  installation_power_kw: "",
  max_pln_budget: "",
  on_roof_installation: true,
  roof_angle: "",
  distance_from_inverter_to_modules_m: "",
  shading_likert: "1",
};
