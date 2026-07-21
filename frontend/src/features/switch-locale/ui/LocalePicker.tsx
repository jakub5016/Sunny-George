import { useEffect, useId, useRef, useState } from "react";
import { useTranslation } from "react-i18next";
import { LOCALES, useLocale, type Locale } from "@shared/lib/i18n";
import { FlagIcon } from "./FlagIcon";
import styles from "./LocalePicker.module.css";

export function LocalePicker() {
  const { locale, setLocale } = useLocale();
  const { t } = useTranslation();
  const [isOpen, setIsOpen] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);
  const menuId = useId();

  useEffect(() => {
    if (!isOpen) {
      return;
    }

    const handlePointerDown = (event: MouseEvent) => {
      if (!containerRef.current?.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };

    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape") {
        setIsOpen(false);
      }
    };

    document.addEventListener("mousedown", handlePointerDown);
    document.addEventListener("keydown", handleKeyDown);

    return () => {
      document.removeEventListener("mousedown", handlePointerDown);
      document.removeEventListener("keydown", handleKeyDown);
    };
  }, [isOpen]);

  const handleSelect = (nextLocale: Locale) => {
    setLocale(nextLocale);
    setIsOpen(false);
  };

  return (
    <div className={styles.picker} ref={containerRef}>
      <button
        type="button"
        className={`${styles.trigger} ${isOpen ? styles.triggerOpen : ""}`}
        aria-haspopup="listbox"
        aria-expanded={isOpen}
        aria-controls={menuId}
        onClick={() => setIsOpen((open) => !open)}
      >
        <FlagIcon locale={locale} className={styles.triggerFlag} />
        <span>{t("locale.pickerLabel")}</span>
      </button>

      {isOpen && (
        <div
          id={menuId}
          className={styles.menu}
          role="listbox"
          aria-label={t("locale.pickerAriaLabel")}
        >
          {LOCALES.map((optionLocale) => (
            <button
              key={optionLocale}
              type="button"
              role="option"
              aria-selected={locale === optionLocale}
              className={`${styles.option} ${
                locale === optionLocale ? styles.optionActive : ""
              }`}
              onClick={() => handleSelect(optionLocale)}
            >
              <FlagIcon locale={optionLocale} className={styles.optionFlag} />
              <span>{t(`locale.options.${optionLocale}`)}</span>
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
