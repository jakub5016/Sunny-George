import { useCallback, useState } from "react";
import { useTranslation } from "react-i18next";
import type { PvInstallation } from "@entities/pv-installation";
import { designPvInstallation } from "../api/designPvInstallation";
import { mapFormToRequest } from "../lib/mapFormToRequest";
import type { PvDesignFormValues } from "./types";

export type { PvDesignFormValues } from "./types";

export function useDesignPvInstallation() {
  const { t } = useTranslation();
  const [matchingInstallations, setMatchingInstallations] = useState<PvInstallation[]>(
    [],
  );
  const [alternativeInstallations, setAlternativeInstallations] = useState<
    PvInstallation[]
  >([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [hasSubmitted, setHasSubmitted] = useState(false);

  const design = useCallback(async (values: PvDesignFormValues) => {
    setIsLoading(true);
    setError(null);
    setHasSubmitted(true);

    try {
      const response = await designPvInstallation(mapFormToRequest(values));
      setMatchingInstallations(response.matching_installations);
      setAlternativeInstallations(response.alternative_installations);
    } catch (err) {
      setMatchingInstallations([]);
      setAlternativeInstallations([]);
      setError(
        err instanceof Error ? err.message : t("pvDesigner.error.generic"),
      );
    } finally {
      setIsLoading(false);
    }
  }, [t]);

  return {
    matchingInstallations,
    alternativeInstallations,
    isLoading,
    error,
    hasSubmitted,
    design,
  };
}
