export interface ClientRequirements {
  installation_area_m2: number;
  installation_power_kw: number;
  max_pln_budget: number;
}

export type ShadingLikert = 1 | 2 | 3 | 4 | 5;

export interface InstallationSite {
  roof_angle: number | null;
  on_roof_installation: boolean;
  installation_area_m2: number;
  distance_from_inverter_to_modules_m: number;
  shading_likert: ShadingLikert;
}

export interface PvModule {
  id: number;
  name: string;
  power_watt: number;
  efficiency_percent: number;
  price_pln: number;
  height_cm: number;
  width_cm: number;
  voc: number;
  vmp: number;
  Imp: number;
  temperature_coefficient_percent_per_c: number;
}

export interface Inverter {
  id: number;
  name: string;
  price_pln: number;
  max_dc_voltage: number;
  mppt_min: number;
  mppt_max: number;
  max_dc_power: number;
  phases: string;
  max_mppt_current: number;
}

export interface InstallationMetrics {
  installation_area_m2: number;
  installation_power_kw: number;
  total_cost_pln: number;
}

export interface PvInstallation {
  inverter: Inverter;
  module_type: PvModule;
  module_count: number;
  match_percent: number;
  metrics: InstallationMetrics;
}

export interface PvDesignResponse {
  matching_installations: PvInstallation[];
  alternative_installations: PvInstallation[];
}
