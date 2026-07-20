import { useTranslation } from "react-i18next";
import { Logo } from "@shared/ui/logo";
import styles from "./LoadingState.module.css";

interface LoadingStateProps {
  message?: string;
}

export function LoadingState({ message }: LoadingStateProps) {
  const { t } = useTranslation();

  return (
    <div className={styles.container} role="status" aria-live="polite">
      <Logo size="lg" className={styles.logo} />
      <p className={styles.message}>{message ?? t("common.loading")}</p>
    </div>
  );
}
