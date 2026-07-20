import { useTranslation } from "react-i18next";
import { LocalePicker } from "@features/switch-locale";
import { ThemeToggle } from "@features/toggle-theme";
import { AppViewNav, type AppView } from "@features/switch-app-view";
import { Logo } from "@shared/ui/logo";
import styles from "./AppHeader.module.css";

interface AppHeaderProps {
  activeView: AppView;
  onViewChange: (view: AppView) => void;
}

export function AppHeader({ activeView, onViewChange }: AppHeaderProps) {
  const { t } = useTranslation();

  return (
    <header className={styles.header}>
      <div className={styles.inner}>
        <div className={styles.brand}>
          <Logo size="md" />
          <div className={styles.titles}>
            <h1 className={styles.title}>{t("header.title")}</h1>
            <p className={styles.subtitle}>{t("header.subtitle")}</p>
          </div>
        </div>

        <div className={styles.actions}>
          <AppViewNav activeView={activeView} onViewChange={onViewChange} />
          <LocalePicker />
          <ThemeToggle />
        </div>
      </div>
    </header>
  );
}
