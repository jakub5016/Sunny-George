import { useEffect, useRef, type RefObject } from "react";
import { Trans, useTranslation } from "react-i18next";
import type { PvInstallation } from "@entities/pv-installation";
import { getMatchLevel } from "@entities/pv-installation";
import styles from "./InstallationResults.module.css";

const MATCH_VALUE_CLASS = {
  high: styles.matchValueHigh,
  medium: styles.matchValueMedium,
  low: styles.matchValueLow,
} as const;

interface InstallationResultsProps {
  matchingInstallations: PvInstallation[];
  alternativeInstallations: PvInstallation[];
  hasSubmitted: boolean;
}

function formatNumber(
  value: number,
  locale: string,
  maximumFractionDigits = 1,
): string {
  return value.toLocaleString(locale, { maximumFractionDigits });
}

function formatCurrency(value: number, locale: string): string {
  return value.toLocaleString(locale, {
    style: "currency",
    currency: "PLN",
    maximumFractionDigits: 0,
  });
}

interface InstallationCardProps {
  installation: PvInstallation;
  locale: string;
  scrollRef?: RefObject<HTMLElement | null>;
}

function InstallationCard({
  installation,
  locale,
  scrollRef,
}: InstallationCardProps) {
  const { t } = useTranslation();
  const matchPercent = installation.match_percent;
  const matchValueClass = MATCH_VALUE_CLASS[getMatchLevel(matchPercent)];

  return (
    <article ref={scrollRef} className={styles.card}>
      <p className={styles.matchBanner}>
        <Trans
          i18nKey="pvDesigner.results.matchBanner"
          values={{ percent: matchPercent }}
          components={{
            highlight: <span className={matchValueClass} />,
          }}
        />
      </p>

      <dl className={styles.details}>
        <div className={styles.detailRow}>
          <dt className={styles.detailLabel}>
            {t("pvDesigner.results.moduleLabel")}
          </dt>
          <dd className={styles.detailValue}>{installation.module_type.name}</dd>
        </div>
        <div className={styles.detailRow}>
          <dt className={styles.detailLabel}>
            {t("pvDesigner.results.inverterLabel")}
          </dt>
          <dd className={styles.detailValue}>{installation.inverter.name}</dd>
        </div>
        <div className={styles.detailRow}>
          <dt className={styles.detailLabel}>
            {t("pvDesigner.results.moduleCountLabel")}
          </dt>
          <dd className={styles.detailValue}>{installation.module_count}</dd>
        </div>
      </dl>

      <div className={styles.metrics}>
        <p className={styles.metricsTitle}>
          {t("pvDesigner.results.calculationTitle")}
        </p>
        <div className={styles.detailRow}>
          <span className={styles.detailLabel}>
            {t("pvDesigner.results.areaLabel")}
          </span>
          <span className={styles.detailValue}>
            {t("pvDesigner.results.areaValue", {
              value: formatNumber(
                installation.metrics.installation_area_m2,
                locale,
              ),
            })}
          </span>
        </div>
        <div className={styles.detailRow}>
          <span className={styles.detailLabel}>
            {t("pvDesigner.results.powerLabel")}
          </span>
          <span className={styles.detailValue}>
            {t("pvDesigner.results.powerValue", {
              value: formatNumber(
                installation.metrics.installation_power_kw,
                locale,
              ),
            })}
          </span>
        </div>
        <div className={styles.detailRow}>
          <span className={styles.detailLabel}>
            {t("pvDesigner.results.costLabel")}
          </span>
          <span className={styles.detailValue}>
            {formatCurrency(installation.metrics.total_cost_pln, locale)}
          </span>
        </div>
      </div>
    </article>
  );
}

export function InstallationResults({
  matchingInstallations,
  alternativeInstallations,
  hasSubmitted,
}: InstallationResultsProps) {
  const { t, i18n } = useTranslation();
  const locale = i18n.language.startsWith("pl") ? "pl-PL" : "en-US";
  const firstResultRef = useRef<HTMLElement>(null);

  const hasMatching = matchingInstallations.length > 0;
  const hasAlternatives = alternativeInstallations.length > 0;
  const showAlternatives = !hasMatching && hasAlternatives;

  useEffect(() => {
    if (!hasMatching && !showAlternatives) {
      return;
    }

    firstResultRef.current?.scrollIntoView({
      behavior: "smooth",
      block: "start",
    });
  }, [matchingInstallations, alternativeInstallations, hasMatching, showAlternatives]);

  if (!hasSubmitted) {
    return null;
  }

  if (!hasMatching && !hasAlternatives) {
    return <p className={styles.empty}>{t("pvDesigner.results.empty")}</p>;
  }

  return (
    <>
      {!hasMatching && (
        <p className={styles.empty}>{t("pvDesigner.results.empty")}</p>
      )}

      {hasMatching && (
        <section
          className={styles.list}
          aria-label={t("pvDesigner.results.ariaLabel")}
        >
          <h3 className={styles.heading}>
            {matchingInstallations.length === 1
              ? t("pvDesigner.results.singleHeading")
              : t("pvDesigner.results.multipleHeading", {
                  count: matchingInstallations.length,
                })}
          </h3>

          {matchingInstallations.map((installation, index) => (
            <InstallationCard
              key={`${installation.module_type.id}-${installation.inverter.id}-${installation.module_count}-${index}`}
              installation={installation}
              locale={locale}
              scrollRef={index === 0 ? firstResultRef : undefined}
            />
          ))}
        </section>
      )}

      {showAlternatives && (
        <section
          className={styles.list}
          aria-label={t("pvDesigner.results.alternativeAriaLabel")}
        >
          <h3 className={styles.heading}>
            {t("pvDesigner.results.alternativeHeading")}
          </h3>
          <p className={styles.alternativeDescription}>
            {t("pvDesigner.results.alternativeDescription")}
          </p>

          {alternativeInstallations.map((installation, index) => (
            <InstallationCard
              key={`${installation.module_type.id}-${installation.inverter.id}-${installation.module_count}-${index}`}
              installation={installation}
              locale={locale}
              scrollRef={index === 0 ? firstResultRef : undefined}
            />
          ))}
        </section>
      )}
    </>
  );
}
