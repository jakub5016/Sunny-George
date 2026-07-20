import { useState } from "react";
import { ChatPage } from "@pages/chat";
import { PvDesignerPage } from "@pages/pv-designer";
import { CatalogPage } from "@pages/catalog";
import { LocaleProvider } from "@shared/lib/i18n";
import { ThemeProvider } from "@shared/lib/theme";
import type { AppView } from "@features/switch-app-view";
import { AppHeader } from "@widgets/app-header";
import styles from "./App.module.css";

export function App() {
  const [view, setView] = useState<AppView>("chat");

  return (
    <ThemeProvider>
      <LocaleProvider>
        <div className={styles.page}>
          <AppHeader activeView={view} onViewChange={setView} />
          <div className={styles.content}>
            {view === "chat" && <ChatPage />}
            {view === "designer" && <PvDesignerPage />}
            {view === "catalog" && <CatalogPage />}
          </div>
        </div>
      </LocaleProvider>
    </ThemeProvider>
  );
}
