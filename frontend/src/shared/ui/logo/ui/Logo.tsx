import megaWattLogo from "@shared/assets/MegaWatt.png";
import styles from "./Logo.module.css";

interface LogoProps {
  size?: "sm" | "md" | "lg";
  className?: string;
}

const sizeClass = {
  sm: styles.sm,
  md: styles.md,
  lg: styles.lg,
} as const;

export function Logo({ size = "md", className }: LogoProps) {
  const classes = [styles.logo, sizeClass[size], className].filter(Boolean).join(" ");

  return (
    <img
      src={megaWattLogo}
      alt="MegaWatt"
      className={classes}
    />
  );
}
