import { useTranslation } from "react-i18next";
import type { AppView } from "../model/types";
import styles from "./AppViewNav.module.css";

interface AppViewNavProps {
  activeView: AppView;
  onViewChange: (view: AppView) => void;
}

const VIEWS: AppView[] = ["chat", "designer", "catalog"];

export function AppViewNav({ activeView, onViewChange }: AppViewNavProps) {
  const { t } = useTranslation();

  return (
    <nav className={styles.nav} aria-label={t("nav.ariaLabel")}>
      {VIEWS.map((id) => (
        <button
          key={id}
          type="button"
          className={`${styles.tab} ${activeView === id ? styles.tabActive : ""}`}
          aria-current={activeView === id ? "page" : undefined}
          onClick={() => onViewChange(id)}
        >
          {t(`nav.${id}`)}
        </button>
      ))}
    </nav>
  );
}
