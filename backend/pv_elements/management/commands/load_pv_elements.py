import csv
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from pv_design.services.genetic_algorithm.ga_data_cache import GADataCache
from pv_elements.models.inverter import Inverter
from pv_elements.models.pv_module import PvModule
from pv_elements.models.types.phase_type import PhaseType


class Command(BaseCommand):
    help = "Loads PV modules and inverters from CSV files into the database."

    def add_arguments(self, parser):
        default_data_dir = Path(__file__).resolve().parents[2] / "example_data" 

        parser.add_argument(
            "--data-dir",
            type=str,
            default=str(default_data_dir),
            help="Directory containing modules.csv and inverters.csv",
        )
        parser.add_argument(
            "--modules-file",
            type=str,
            default=None,
            help="Path to modules CSV (overrides --data-dir/modules.csv)",
        )
        parser.add_argument(
            "--inverters-file",
            type=str,
            default=None,
            help="Path to inverters CSV (overrides --data-dir/inverters.csv)",
        )

    def handle(self, *args, **options):
        data_dir = Path(options["data_dir"])
        modules_path = Path(options["modules_file"]) if options["modules_file"] else data_dir / "modules.csv"
        inverters_path = (
            Path(options["inverters_file"]) if options["inverters_file"] else data_dir / "inverters.csv"
        )

        for csv_path in (modules_path, inverters_path):
            if not csv_path.exists():
                raise CommandError(f"File does not exist: {csv_path}")

        modules_created = self._load_modules(modules_path)
        inverters_created = self._load_inverters(inverters_path)

        GADataCache().clear_cache()

        self.stdout.write(self.style.SUCCESS(
            f"Loaded CSV data: {modules_created} new modules, "
            f"{inverters_created} new inverters "
            f"({PvModule.objects.count()} modules and "
            f"{Inverter.objects.count()} inverters in database)."
        ))

    def _load_modules(self, csv_path: Path) -> int:
        loaded = 0
        with open(csv_path, encoding="utf-8") as file:
            for row in csv.DictReader(file):
                _, created = PvModule.objects.get_or_create(
                    name=row["name"],
                    defaults={
                        "power_watt": float(row["power_watt"]),
                        "efficiency_percent": float(row["efficiency_percent"]),
                        "price_pln": float(row["price_pln"]),
                        "height_cm": float(row["height_cm"]),
                        "width_cm": float(row["width_cm"]),
                        "voc": float(row["voc"]),
                        "vmp": float(row["vmp"]),
                        "Imp": float(row["Imp"]),
                        "temperature_coefficient_percent_per_c": float(
                            row["temperature_coefficient_percent_per_c"]
                        ),
                    },
                )
                if created:
                    loaded += 1
        return loaded

    def _load_inverters(self, csv_path: Path) -> int:
        loaded = 0
        with open(csv_path, encoding="utf-8") as file:
            for row in csv.DictReader(file):
                phases = row["phases"]
                if phases not in PhaseType.values:
                    raise CommandError(
                        f"Invalid phases value '{phases}' in {csv_path.name}. "
                        f"Use one of: {', '.join(PhaseType.values)}"
                    )

                _, created = Inverter.objects.get_or_create(
                    name=row["name"],
                    defaults={
                        "price_pln": float(row["price_pln"]),
                        "max_dc_voltage": float(row["max_dc_voltage"]),
                        "mppt_min": float(row["mppt_min"]),
                        "mppt_max": float(row["mppt_max"]),
                        "max_dc_power": float(row["max_dc_power"]),
                        "phases": phases,
                        "max_mppt_current": float(row["max_mppt_current"]),
                    },
                )
                if created:
                    loaded += 1
        return loaded
