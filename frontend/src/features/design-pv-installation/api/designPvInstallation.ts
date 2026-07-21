import { apiRequest } from "@shared/api/client";
import type {
  ClientRequirements,
  InstallationSite,
  PvDesignResponse,
} from "@entities/pv-installation";

export interface DesignPvInstallationRequest {
  client_requirements: ClientRequirements;
  installation_site: InstallationSite;
  generations?: number;
  population_size?: number;
}

export async function designPvInstallation(
  payload: DesignPvInstallationRequest,
): Promise<PvDesignResponse> {
  return apiRequest<PvDesignResponse>("/api/pv-design/design/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
}
