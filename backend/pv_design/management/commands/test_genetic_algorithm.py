import csv
import random
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from pv_design.dto.client_requirements import ClientRequirementsDto
from pv_design.dto.installation_site_dto import InstallationSiteDto
from pv_design.services.genetic_algorithm.fitness_service import FitnessService
from pv_design.services.installation_checker import InstallationChecker
from pv_design.services.client_expectations_checker import ClientExpectationsChecker
from pv_design.services.requirements_match_service import RequirementsMatchService
from pv_design.services.pv_installation_designer import PvInstallationDesigner
from pv_elements.models.inverter import Inverter
from pv_elements.models.pv_module import PvModule


class Command(BaseCommand):
    help = (
        "Runs the genetic algorithm against PV modules and inverters already stored "
        "in the database. Does not modify the database."
    )

    def add_arguments(self, parser):
        default_requirements_file = (
            Path(__file__).resolve().parents[2] / "data" / "ga_test" / "requirements.csv"
        )

        parser.add_argument(
            "--requirements-file",
            type=str,
            default=str(default_requirements_file),
            help="CSV file with client requirements (used when --area/--power/--budget not set)",
        )
        parser.add_argument(
            "--area",
            type=float,
            default=None,
            help="Required installation area in m2",
        )
        parser.add_argument(
            "--power",
            type=float,
            default=None,
            help="Required installation power in kW",
        )
        parser.add_argument(
            "--budget",
            type=float,
            default=None,
            help="Maximum budget in PLN",
        )
        parser.add_argument(
            "--generations",
            type=int,
            default=None,
            help="Override number of GA generations (default: from env/const)",
        )
        parser.add_argument(
            "--population-size",
            type=int,
            default=None,
            help="Override GA population size (default: from env/const)",
        )
        parser.add_argument(
            "--seed",
            type=int,
            default=42,
            help="Random seed for reproducible GA runs (default: 42)",
        )

    def handle(self, *args, **options):
        module_count = PvModule.objects.count()
        inverter_count = Inverter.objects.count()

        if module_count == 0 or inverter_count == 0:
            raise CommandError(
                "Database has no PV modules or inverters. "
                "Load sample data first: python manage.py load_pv_elements"
            )

        if options["seed"] is not None:
            random.seed(options["seed"])

        requirements = self._resolve_requirements(options)

        self.stdout.write(
            f"Using {module_count} modules and {inverter_count} inverters from the database."
        )
        self._print_requirements(requirements)

        designer = PvInstallationDesigner()
        result = self._run_designer(designer, requirements, options)

        if not result.matching_installations and not result.alternative_installations:
            self.stdout.write(
                self.style.ERROR("GA did not find valid installations.")
            )
            return

        installation_site = self._default_installation_site()

        if result.matching_installations:
            for index, installation in enumerate(result.matching_installations, start=1):
                self.stdout.write(self.style.SUCCESS(f"\nMatching proposal {index}:"))
                self._print_result(installation, requirements, installation_site)

        if result.alternative_installations:
            for index, installation in enumerate(result.alternative_installations, start=1):
                self.stdout.write(self.style.WARNING(f"\nAlternative proposal {index}:"))
                self._print_result(installation, requirements, installation_site)

    def _resolve_requirements(self, options: dict) -> ClientRequirementsDto:
        cli_values = {
            "installation_area_m2": options["area"],
            "installation_power_kw": options["power"],
            "max_pln_budget": options["budget"],
        }

        if all(value is not None for value in cli_values.values()):
            return ClientRequirementsDto(**cli_values)

        if any(value is not None for value in cli_values.values()):
            raise CommandError(
                "Provide all of --area, --power and --budget together, "
                "or omit them to use --requirements-file."
            )

        requirements_path = Path(options["requirements_file"])
        if not requirements_path.exists():
            raise CommandError(f"Requirements file does not exist: {requirements_path}")

        return self._load_requirements(requirements_path)

    def _load_requirements(self, csv_path: Path) -> ClientRequirementsDto:
        with open(csv_path, encoding="utf-8") as file:
            rows = list(csv.DictReader(file))

        if not rows:
            raise CommandError(f"No requirements found in {csv_path}")

        row = rows[0]
        return ClientRequirementsDto(
            installation_area_m2=float(row["installation_area_m2"]),
            installation_power_kw=float(row["installation_power_kw"]),
            max_pln_budget=float(row["max_pln_budget"]),
        )

    def _run_designer(
        self,
        designer: PvInstallationDesigner,
        requirements: ClientRequirementsDto,
        options: dict,
    ):
        ga_kwargs = {}
        if options["generations"] is not None:
            ga_kwargs["generations"] = options["generations"]
        if options["population_size"] is not None:
            ga_kwargs["population_size"] = options["population_size"]

        return designer.design(requirements, self._default_installation_site(), **ga_kwargs)

    def _default_installation_site(self) -> InstallationSiteDto:
        return InstallationSiteDto(
            roof_angle=30.0,
            on_roof_installation=True,
            installation_area_m2=50.0,
            distance_from_inverter_to_modules_m=10.0,
            shading_likert=1,
        )

    def _print_requirements(self, requirements: ClientRequirementsDto) -> None:
        self.stdout.write("\nClient requirements:")
        self.stdout.write(f"  Area:   {requirements.installation_area_m2} m2")
        self.stdout.write(f"  Power:  {requirements.installation_power_kw} kW")
        self.stdout.write(f"  Budget: {requirements.max_pln_budget} PLN")
        self.stdout.write("Running genetic algorithm...\n")

    def _print_result(
        self,
        installation,
        requirements: ClientRequirementsDto,
        installation_site: InstallationSiteDto,
    ) -> None:
        metrics = InstallationMetricsService().calculate(installation, installation_site)
        fitness = FitnessService().calculate(installation, requirements, installation_site)
        match_percent = RequirementsMatchService().calculate_percent(
            installation, requirements, installation_site
        )
        is_valid = InstallationChecker().check(installation)
        meets_expectations = ClientExpectationsChecker().check(
            installation, requirements, installation_site
        )

        self.stdout.write("  Installation details:")
        self.stdout.write(f"  Module:   {installation.module_type.name}")
        self.stdout.write(f"  Inverter: {installation.inverter.name}")
        self.stdout.write(f"  Modules:  {installation.module_count}")
        self.stdout.write(f"  Valid:    {is_valid}")
        self.stdout.write(f"  Meets client expectations: {meets_expectations}")
        self.stdout.write(f"  Fitness:  {fitness:.6f}")
        self.stdout.write(f"  Match:    {match_percent}%")
        self.stdout.write("\nResult metrics vs requirements:")
        self.stdout.write(
            f"  Area:   {metrics.installation_area_m2:.2f} m2 "
            f"(target {requirements.installation_area_m2} m2)"
        )
        self.stdout.write(
            f"  Power:  {metrics.installation_power_kw:.2f} kW "
            f"(target {requirements.installation_power_kw} kW)"
        )
        self.stdout.write(
            f"  Cost:   {metrics.total_cost_pln:.2f} PLN "
            f"(target {requirements.max_pln_budget} PLN)"
        )
