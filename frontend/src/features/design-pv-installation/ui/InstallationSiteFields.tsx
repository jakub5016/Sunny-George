import { useTranslation } from "react-i18next";
import {
  getShadingLikertLabelKey,
  SHADING_LIKERT_OPTIONS,
} from "@entities/pv-installation";
import type { PvDesignFormValues } from "../model/types";
import styles from "./PvRequirementsForm.module.css";

interface InstallationSiteFieldsProps {
  values: PvDesignFormValues;
  disabled?: boolean;
  onChange: <K extends keyof PvDesignFormValues>(
    field: K,
    value: PvDesignFormValues[K],
  ) => void;
}

export function InstallationSiteFields({
  values,
  disabled = false,
  onChange,
}: InstallationSiteFieldsProps) {
  const { t } = useTranslation();

  return (
    <fieldset className={styles.section}>
      <legend className={styles.sectionTitle}>
        {t("pvDesigner.form.siteSectionTitle")}
      </legend>
      <p className={styles.sectionDescription}>
        {t("pvDesigner.form.siteSectionDescription")}
      </p>

      <div className={styles.fields}>
        <div className={styles.field}>
          <span className={styles.label} id="installation-type-label">
            {t("pvDesigner.form.installationTypeLabel")}
          </span>
          <div
            className={styles.radioGroup}
            role="radiogroup"
            aria-labelledby="installation-type-label"
          >
            <label className={styles.radioOption}>
              <input
                type="radio"
                name="installation-type"
                checked={values.on_roof_installation}
                disabled={disabled}
                onChange={() => onChange("on_roof_installation", true)}
              />
              <span>{t("pvDesigner.form.installationTypeRoof")}</span>
            </label>
            <label className={styles.radioOption}>
              <input
                type="radio"
                name="installation-type"
                checked={!values.on_roof_installation}
                disabled={disabled}
                onChange={() => onChange("on_roof_installation", false)}
              />
              <span>{t("pvDesigner.form.installationTypeGround")}</span>
            </label>
          </div>
        </div>

        {values.on_roof_installation && (
          <div className={styles.field}>
            <label className={styles.label} htmlFor="roof-angle">
              {t("pvDesigner.form.roofAngleLabel")}
            </label>
            <input
              id="roof-angle"
              className={styles.input}
              type="number"
              min="0"
              max="90"
              step="1"
              placeholder={t("pvDesigner.form.roofAnglePlaceholder")}
              disabled={disabled}
              value={values.roof_angle}
              onChange={(event) => onChange("roof_angle", event.target.value)}
            />
          </div>
        )}

        <div className={styles.field}>
          <label className={styles.label} htmlFor="cable-distance">
            {t("pvDesigner.form.cableDistanceLabel")}
          </label>
          <input
            id="cable-distance"
            className={styles.input}
            type="number"
            min="0"
            step="0.1"
            placeholder={t("pvDesigner.form.cableDistancePlaceholder")}
            disabled={disabled}
            value={values.distance_from_inverter_to_modules_m}
            onChange={(event) =>
              onChange("distance_from_inverter_to_modules_m", event.target.value)
            }
          />
        </div>

        <div className={styles.field}>
          <label className={styles.label} htmlFor="shading-likert">
            {t("pvDesigner.form.shadingLabel")}
          </label>
          <select
            id="shading-likert"
            className={styles.select}
            disabled={disabled}
            value={values.shading_likert}
            onChange={(event) => onChange("shading_likert", event.target.value)}
          >
            {SHADING_LIKERT_OPTIONS.map((option) => (
              <option key={option} value={option}>
                {t(getShadingLikertLabelKey(option))}
              </option>
            ))}
          </select>
        </div>
      </div>
    </fieldset>
  );
}
