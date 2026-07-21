import { useEffect, useState, useCallback } from "react";
import { useTranslation } from "react-i18next";
import {
  fetchModules,
  fetchInverters,
  type PvModule,
  type Inverter,
  type ModuleFilters,
  type InverterFilters,
} from "@shared/api/catalog";
import styles from "./CatalogPage.module.css";

type CatalogTab = "modules" | "inverters";

const SOLAR_PANEL_ICON = (
  <svg
    width="40"
    height="40"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="1.5"
    aria-hidden="true"
  >
    <rect x="2" y="5" width="20" height="14" rx="1" />
    <line x1="7" y1="5" x2="7" y2="19" />
    <line x1="12" y1="5" x2="12" y2="19" />
    <line x1="17" y1="5" x2="17" y2="19" />
    <line x1="2" y1="10" x2="22" y2="10" />
    <line x1="2" y1="15" x2="22" y2="15" />
  </svg>
);

const INVERTER_ICON = (
  <svg
    width="40"
    height="40"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="1.5"
    aria-hidden="true"
  >
    <rect x="3" y="6" width="18" height="12" rx="2" />
    <circle cx="8" cy="12" r="1.5" />
    <line x1="12" y1="9" x2="12" y2="15" />
    <line x1="15" y1="9" x2="15" y2="15" />
    <line x1="18" y1="9" x2="18" y2="12" />
  </svg>
);

function useDebounce<T>(value: T, delay = 400): T {
  const [debounced, setDebounced] = useState(value);
  useEffect(() => {
    const id = setTimeout(() => setDebounced(value), delay);
    return () => clearTimeout(id);
  }, [value, delay]);
  return debounced;
}

function RangeFilter({
  label,
  minValue,
  maxValue,
  onMinChange,
  onMaxChange,
  placeholder,
}: {
  label: string;
  minValue: string;
  maxValue: string;
  onMinChange: (v: string) => void;
  onMaxChange: (v: string) => void;
  placeholder: { min: string; max: string };
}) {
  return (
    <div className={styles.filterGroup}>
      <label className={styles.filterLabel}>{label}</label>
      <div className={styles.rangeInputs}>
        <input
          type="number"
          className={styles.filterInput}
          value={minValue}
          onChange={(e) => onMinChange(e.target.value)}
          placeholder={placeholder.min}
          min={0}
        />
        <span className={styles.rangeSep}>–</span>
        <input
          type="number"
          className={styles.filterInput}
          value={maxValue}
          onChange={(e) => onMaxChange(e.target.value)}
          placeholder={placeholder.max}
          min={0}
        />
      </div>
    </div>
  );
}

function ModuleCard({ module }: { module: PvModule }) {
  const { t } = useTranslation();
  return (
    <article className={styles.card}>
      <div className={styles.cardImage}>
        {module.image ? (
          <img src={module.image} alt={module.name} className={styles.productImage} />
        ) : (
          <div className={styles.cardImagePlaceholder}>{SOLAR_PANEL_ICON}</div>
        )}
      </div>
      <div className={styles.cardBody}>
        <h3 className={styles.cardTitle}>{module.name}</h3>
        <dl className={styles.cardSpecs}>
          <div className={styles.specRow}>
            <dt>{t("catalog.module.power")}</dt>
            <dd className={styles.specHighlight}>{module.power_watt} W</dd>
          </div>
          <div className={styles.specRow}>
            <dt>{t("catalog.module.efficiency")}</dt>
            <dd>{module.efficiency_percent.toFixed(1)} %</dd>
          </div>
          <div className={styles.specRow}>
            <dt>{t("catalog.module.voc")}</dt>
            <dd>{module.voc} V</dd>
          </div>
          <div className={styles.specRow}>
            <dt>{t("catalog.module.vmp")}</dt>
            <dd>{module.vmp} V</dd>
          </div>
          <div className={styles.specRow}>
            <dt>{t("catalog.module.dimensions")}</dt>
            <dd>
              {module.height_cm} × {module.width_cm} cm
            </dd>
          </div>
        </dl>
        <div className={styles.cardFooter}>
          <span className={styles.price}>
            {module.price_pln.toLocaleString("pl-PL")} PLN
          </span>
        </div>
      </div>
    </article>
  );
}

function InverterCard({ inverter }: { inverter: Inverter }) {
  const { t } = useTranslation();
  return (
    <article className={styles.card}>
      <div className={styles.cardImage}>
        {inverter.image ? (
          <img src={inverter.image} alt={inverter.name} className={styles.productImage} />
        ) : (
          <div className={styles.cardImagePlaceholder}>{INVERTER_ICON}</div>
        )}
      </div>
      <div className={styles.cardBody}>
        <h3 className={styles.cardTitle}>{inverter.name}</h3>
        <dl className={styles.cardSpecs}>
          <div className={styles.specRow}>
            <dt>{t("catalog.inverter.maxDcPower")}</dt>
            <dd className={styles.specHighlight}>
              {(inverter.max_dc_power / 1000).toFixed(1)} kW
            </dd>
          </div>
          <div className={styles.specRow}>
            <dt>{t("catalog.inverter.phases")}</dt>
            <dd>{inverter.phases_display}</dd>
          </div>
          <div className={styles.specRow}>
            <dt>{t("catalog.inverter.mpptRange")}</dt>
            <dd>
              {inverter.mppt_min}–{inverter.mppt_max} V
            </dd>
          </div>
          <div className={styles.specRow}>
            <dt>{t("catalog.inverter.maxDcVoltage")}</dt>
            <dd>{inverter.max_dc_voltage} V</dd>
          </div>
        </dl>
        <div className={styles.cardFooter}>
          <span className={styles.price}>
            {inverter.price_pln.toLocaleString("pl-PL")} PLN
          </span>
        </div>
      </div>
    </article>
  );
}

export function CatalogPage() {
  const { t } = useTranslation();
  const [tab, setTab] = useState<CatalogTab>("modules");

  const [modules, setModules] = useState<PvModule[]>([]);
  const [inverters, setInverters] = useState<Inverter[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [modFilters, setModFilters] = useState({
    search: "",
    power_min: "",
    power_max: "",
    efficiency_min: "",
    efficiency_max: "",
    price_min: "",
    price_max: "",
  });

  const [invFilters, setInvFilters] = useState({
    search: "",
    phases: "" as "" | "single" | "three",
    power_min: "",
    power_max: "",
    price_min: "",
    price_max: "",
  });

  const debouncedModFilters = useDebounce(modFilters);
  const debouncedInvFilters = useDebounce(invFilters);

  const loadModules = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const filters: ModuleFilters = {
        search: debouncedModFilters.search || undefined,
        power_min: debouncedModFilters.power_min
          ? Number(debouncedModFilters.power_min)
          : undefined,
        power_max: debouncedModFilters.power_max
          ? Number(debouncedModFilters.power_max)
          : undefined,
        efficiency_min: debouncedModFilters.efficiency_min
          ? Number(debouncedModFilters.efficiency_min)
          : undefined,
        efficiency_max: debouncedModFilters.efficiency_max
          ? Number(debouncedModFilters.efficiency_max)
          : undefined,
        price_min: debouncedModFilters.price_min
          ? Number(debouncedModFilters.price_min)
          : undefined,
        price_max: debouncedModFilters.price_max
          ? Number(debouncedModFilters.price_max)
          : undefined,
      };
      setModules(await fetchModules(filters));
    } catch {
      setError(t("catalog.error"));
    } finally {
      setLoading(false);
    }
  }, [debouncedModFilters, t]);

  const loadInverters = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const filters: InverterFilters = {
        search: debouncedInvFilters.search || undefined,
        phases: debouncedInvFilters.phases || undefined,
        power_min: debouncedInvFilters.power_min
          ? Number(debouncedInvFilters.power_min)
          : undefined,
        power_max: debouncedInvFilters.power_max
          ? Number(debouncedInvFilters.power_max)
          : undefined,
        price_min: debouncedInvFilters.price_min
          ? Number(debouncedInvFilters.price_min)
          : undefined,
        price_max: debouncedInvFilters.price_max
          ? Number(debouncedInvFilters.price_max)
          : undefined,
      };
      setInverters(await fetchInverters(filters));
    } catch {
      setError(t("catalog.error"));
    } finally {
      setLoading(false);
    }
  }, [debouncedInvFilters, t]);

  useEffect(() => {
    if (tab === "modules") loadModules();
  }, [tab, loadModules]);

  useEffect(() => {
    if (tab === "inverters") loadInverters();
  }, [tab, loadInverters]);

  const setMod = (key: keyof typeof modFilters) => (value: string) =>
    setModFilters((f) => ({ ...f, [key]: value }));

  const setInv =
    (key: keyof typeof invFilters) =>
    (value: string | number) =>
      setInvFilters((f) => ({ ...f, [key]: value }));

  const resultCount = tab === "modules" ? modules.length : inverters.length;

  return (
    <main className={styles.page}>
      <div className={styles.header}>
        <h2 className={styles.heading}>{t("catalog.title")}</h2>
        <p className={styles.subtitle}>{t("catalog.subtitle")}</p>
        <div className={styles.tabs} role="tablist" aria-label={t("catalog.tabsLabel")}>
          <button
            role="tab"
            type="button"
            aria-selected={tab === "modules"}
            className={`${styles.tab} ${tab === "modules" ? styles.tabActive : ""}`}
            onClick={() => setTab("modules")}
          >
            {t("catalog.tabs.modules")}
          </button>
          <button
            role="tab"
            type="button"
            aria-selected={tab === "inverters"}
            className={`${styles.tab} ${tab === "inverters" ? styles.tabActive : ""}`}
            onClick={() => setTab("inverters")}
          >
            {t("catalog.tabs.inverters")}
          </button>
        </div>
      </div>

      <div className={styles.layout}>
        <aside className={styles.filters} aria-label={t("catalog.filtersLabel")}>
          <h3 className={styles.filtersTitle}>{t("catalog.filtersTitle")}</h3>

          {tab === "modules" && (
            <>
              <div className={styles.filterGroup}>
                <label className={styles.filterLabel} htmlFor="mod-search">
                  {t("catalog.filter.search")}
                </label>
                <input
                  id="mod-search"
                  type="search"
                  className={styles.filterInput}
                  value={modFilters.search}
                  onChange={(e) => setMod("search")(e.target.value)}
                  placeholder={t("catalog.filter.searchPlaceholder")}
                />
              </div>
              <RangeFilter
                label={t("catalog.module.power") + " (W)"}
                minValue={modFilters.power_min}
                maxValue={modFilters.power_max}
                onMinChange={setMod("power_min")}
                onMaxChange={setMod("power_max")}
                placeholder={{ min: "np. 400", max: "np. 600" }}
              />
              <RangeFilter
                label={t("catalog.module.efficiency") + " (%)"}
                minValue={modFilters.efficiency_min}
                maxValue={modFilters.efficiency_max}
                onMinChange={setMod("efficiency_min")}
                onMaxChange={setMod("efficiency_max")}
                placeholder={{ min: "np. 20", max: "np. 23" }}
              />
              <RangeFilter
                label={t("catalog.filter.price") + " (PLN)"}
                minValue={modFilters.price_min}
                maxValue={modFilters.price_max}
                onMinChange={setMod("price_min")}
                onMaxChange={setMod("price_max")}
                placeholder={{ min: "np. 500", max: "np. 1500" }}
              />
              <button
                type="button"
                className={styles.resetBtn}
                onClick={() =>
                  setModFilters({
                    search: "",
                    power_min: "",
                    power_max: "",
                    efficiency_min: "",
                    efficiency_max: "",
                    price_min: "",
                    price_max: "",
                  })
                }
              >
                {t("catalog.filter.reset")}
              </button>
            </>
          )}

          {tab === "inverters" && (
            <>
              <div className={styles.filterGroup}>
                <label className={styles.filterLabel} htmlFor="inv-search">
                  {t("catalog.filter.search")}
                </label>
                <input
                  id="inv-search"
                  type="search"
                  className={styles.filterInput}
                  value={invFilters.search}
                  onChange={(e) => setInv("search")(e.target.value)}
                  placeholder={t("catalog.filter.searchPlaceholder")}
                />
              </div>
              <div className={styles.filterGroup}>
                <label className={styles.filterLabel} htmlFor="inv-phases">
                  {t("catalog.inverter.phases")}
                </label>
                <select
                  id="inv-phases"
                  className={styles.filterSelect}
                  value={invFilters.phases}
                  onChange={(e) =>
                    setInv("phases")(e.target.value as "" | "single" | "three")
                  }
                >
                  <option value="">{t("catalog.filter.all")}</option>
                  <option value="single">{t("catalog.filter.phaseSingle")}</option>
                  <option value="three">{t("catalog.filter.phaseThree")}</option>
                </select>
              </div>
              <RangeFilter
                label={t("catalog.inverter.maxDcPower") + " (W)"}
                minValue={invFilters.power_min}
                maxValue={invFilters.power_max}
                onMinChange={setInv("power_min")}
                onMaxChange={setInv("power_max")}
                placeholder={{ min: "np. 5000", max: "np. 15000" }}
              />
              <RangeFilter
                label={t("catalog.filter.price") + " (PLN)"}
                minValue={invFilters.price_min}
                maxValue={invFilters.price_max}
                onMinChange={setInv("price_min")}
                onMaxChange={setInv("price_max")}
                placeholder={{ min: "np. 2000", max: "np. 10000" }}
              />
              <button
                type="button"
                className={styles.resetBtn}
                onClick={() =>
                  setInvFilters({
                    search: "",
                    phases: "",
                    power_min: "",
                    power_max: "",
                    price_min: "",
                    price_max: "",
                  })
                }
              >
                {t("catalog.filter.reset")}
              </button>
            </>
          )}
        </aside>

        <section className={styles.results}>
          {error && <p className={styles.errorMsg}>{error}</p>}

          {!error && (
            <p className={styles.resultCount}>
              {t("catalog.resultCount", { count: resultCount })}
            </p>
          )}

          {loading ? (
            <div className={styles.loadingGrid}>
              {Array.from({ length: 6 }).map((_, i) => (
                <div key={i} className={styles.skeletonCard} aria-hidden="true" />
              ))}
            </div>
          ) : (
            <div className={styles.grid}>
              {tab === "modules" &&
                modules.map((m) => <ModuleCard key={m.id} module={m} />)}
              {tab === "inverters" &&
                inverters.map((inv) => (
                  <InverterCard key={inv.id} inverter={inv} />
                ))}
              {!loading && resultCount === 0 && !error && (
                <p className={styles.empty}>{t("catalog.empty")}</p>
              )}
            </div>
          )}
        </section>
      </div>
    </main>
  );
}
