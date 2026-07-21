import { useTranslation } from "react-i18next";
import {
  InstallationResults,
  PvRequirementsForm,
  useDesignPvInstallation,
} from "@features/design-pv-installation";
import { ErrorBanner } from "@shared/ui/error-banner";
import styles from "./PvDesignerPage.module.css";

export function PvDesignerPage() {
  const { t } = useTranslation();
  const {
    matchingInstallations,
    alternativeInstallations,
    isLoading,
    error,
    hasSubmitted,
    design,
  } = useDesignPvInstallation();

  return (
    <main className={styles.page}>
      {error && <ErrorBanner message={error} />}

      <PvRequirementsForm disabled={isLoading} onSubmit={design} />

      {isLoading && (
        <p className={styles.loading} role="status">
          {t("pvDesigner.loading")}
        </p>
      )}

      {!isLoading && (
        <InstallationResults
          matchingInstallations={matchingInstallations}
          alternativeInstallations={alternativeInstallations}
          hasSubmitted={hasSubmitted}
        />
      )}
    </main>
  );
}
