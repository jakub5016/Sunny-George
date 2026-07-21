import { apiRequest } from "./client";

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
  image?: string;
}

export interface Inverter {
  id: number;
  name: string;
  price_pln: number;
  max_dc_voltage: number;
  mppt_min: number;
  mppt_max: number;
  max_dc_power: number;
  phases: "single" | "three";
  phases_display: string;
  max_mppt_current: number;
  image?: string;
}

export interface ModuleFilters {
  search?: string;
  power_min?: number;
  power_max?: number;
  efficiency_min?: number;
  efficiency_max?: number;
  price_min?: number;
  price_max?: number;
}

export interface InverterFilters {
  search?: string;
  phases?: "single" | "three" | "";
  power_min?: number;
  power_max?: number;
  price_min?: number;
  price_max?: number;
}

function buildQuery(filters: Record<string, unknown>): string {
  const params = new URLSearchParams();
  for (const [key, value] of Object.entries(filters)) {
    if (value !== undefined && value !== "" && value !== null) {
      params.set(key, String(value));
    }
  }
  const qs = params.toString();
  return qs ? `?${qs}` : "";
}

export function fetchModules(filters: ModuleFilters = {}): Promise<PvModule[]> {
  return apiRequest<PvModule[]>(`/api/catalog/modules/${buildQuery(filters)}`);
}

export function fetchInverters(
  filters: InverterFilters = {},
): Promise<Inverter[]> {
  return apiRequest<Inverter[]>(
    `/api/catalog/inverters/${buildQuery(filters)}`,
  );
}
