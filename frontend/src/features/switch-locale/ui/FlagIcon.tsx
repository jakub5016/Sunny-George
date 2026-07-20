import type { Locale } from "@shared/lib/i18n";

interface FlagIconProps {
  locale: Locale;
  className?: string;
}

export function FlagIcon({ locale, className }: FlagIconProps) {
  if (locale === "pl") {
    return (
      <svg
        className={className}
        width="20"
        height="14"
        viewBox="0 0 20 14"
        aria-hidden="true"
      >
        <rect width="20" height="7" fill="#FFFFFF" />
        <rect y="7" width="20" height="7" fill="#DC143C" />
        <rect
          width="20"
          height="14"
          fill="none"
          stroke="rgba(10, 35, 66, 0.15)"
        />
      </svg>
    );
  }

  return (
    <svg
      className={className}
      width="20"
      height="14"
      viewBox="0 0 20 14"
      aria-hidden="true"
    >
      <rect width="20" height="14" fill="#012169" />
      <path d="M0 0 20 14M20 0 0 14" stroke="#FFFFFF" strokeWidth="2.2" />
      <path d="M0 0 20 14M20 0 0 14" stroke="#C8102E" strokeWidth="1.2" />
      <path d="M10 0V14M0 7H20" stroke="#FFFFFF" strokeWidth="3.2" />
      <path d="M10 0V14M0 7H20" stroke="#C8102E" strokeWidth="1.8" />
      <rect
        width="20"
        height="14"
        fill="none"
        stroke="rgba(10, 35, 66, 0.15)"
      />
    </svg>
  );
}
