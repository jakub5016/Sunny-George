import { FormEvent, useState } from "react";
import { useTranslation } from "react-i18next";
import { Button } from "@shared/ui/button";
import { isPvDesignFormValid } from "../lib/isPvDesignFormValid";
import {
  INITIAL_PV_DESIGN_FORM_VALUES,
  type PvDesignFormValues,
} from "../model/types";
import { InstallationSiteFields } from "./InstallationSiteFields";
import styles from "./PvRequirementsForm.module.css";

interface PvRequirementsFormProps {
  disabled?: boolean;
  onSubmit: (values: PvDesignFormValues) => void;
}

export function PvRequirementsForm({
  disabled = false,
  onSubmit,
}: PvRequirementsFormProps) {
  const { t } = useTranslation();
  const [values, setValues] = useState<PvDesignFormValues>(
    INITIAL_PV_DESIGN_FORM_VALUES,
  );

  const handleChange = <K extends keyof PvDesignFormValues>(
    field: K,
    value: PvDesignFormValues[K],
  ) => {
    setValues((prev) => ({ ...prev, [field]: value }));
  };

  const handleSubmit = (event: FormEvent) => {
    event.preventDefault();
    onSubmit(values);
  };

  const isValid = isPvDesignFormValid(values);

  return (
    <form className={styles.form} onSubmit={handleSubmit}>
      <div>
        <h2 className={styles.title}>{t("pvDesigner.form.title")}</h2>
        <p className={styles.description}>{t("pvDesigner.form.description")}</p>
      </div>

      <fieldset className={styles.section}>
        <legend className={styles.sectionTitle}>
          {t("pvDesigner.form.requirementsSectionTitle")}
        </legend>

        <div className={styles.fields}>
          <div className={styles.field}>
            <label className={styles.label} htmlFor="installation-area">
              {t("pvDesigner.form.areaLabel")}
            </label>
            <input
              id="installation-area"
              className={styles.input}
              type="number"
              min="0"
              step="0.1"
              placeholder={t("pvDesigner.form.areaPlaceholder")}
              disabled={disabled}
              value={values.installation_area_m2}
              onChange={(event) =>
                handleChange("installation_area_m2", event.target.value)
              }
            />
          </div>

          <div className={styles.field}>
            <label className={styles.label} htmlFor="installation-power">
              {t("pvDesigner.form.powerLabel")}
            </label>
            <input
              id="installation-power"
              className={styles.input}
              type="number"
              min="0"
              step="0.1"
              placeholder={t("pvDesigner.form.powerPlaceholder")}
              disabled={disabled}
              value={values.installation_power_kw}
              onChange={(event) =>
                handleChange("installation_power_kw", event.target.value)
              }
            />
          </div>

          <div className={styles.field}>
            <label className={styles.label} htmlFor="max-budget">
              {t("pvDesigner.form.budgetLabel")}
            </label>
            <input
              id="max-budget"
              className={styles.input}
              type="number"
              min="0"
              step="100"
              placeholder={t("pvDesigner.form.budgetPlaceholder")}
              disabled={disabled}
              value={values.max_pln_budget}
              onChange={(event) =>
                handleChange("max_pln_budget", event.target.value)
              }
            />
          </div>
        </div>
      </fieldset>

      <InstallationSiteFields
        values={values}
        disabled={disabled}
        onChange={handleChange}
      />

      <div className={styles.actions}>
        <Button type="submit" disabled={disabled || !isValid}>
          {t("pvDesigner.form.submit")}
        </Button>
      </div>
    </form>
  );
}
