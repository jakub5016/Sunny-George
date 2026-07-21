from django.test import SimpleTestCase

from config.const import DEFAULT_MIN_TEMP_C
from pv_design.services.installation_checker import InstallationChecker
from pv_design.services.client_expectations_checker import ClientExpectationsChecker
from pv_design.validators.installation.current_input import CurrentInputValidator
from pv_design.validators.installation.dc_power_inverter import DcPowerInverterValidator
from pv_design.validators.installation.max_inverter_dc_voltage import MaxInverterDcVoltageValidator
from pv_design.validators.installation.mppt_max import MpptMaxValidator
from pv_design.validators.installation.mppt_min import MpptMinValidator
from pv_design.validators.client_expectations.max_area_validator import MaxAreaValidator
from pv_design.validators.client_expectations.max_price_validator import MaxPriceValidator
from pv_design.validators.client_expectations.min_power_validator import MinPowerValidator

from .fixtures import make_inverter, make_installation, make_installation_site, make_module, make_requirements


class InstallationValidatorTests(SimpleTestCase):
    def setUp(self) -> None:
        self.installation = make_installation()

    def test_current_input_valid(self) -> None:
        self.assertTrue(CurrentInputValidator().validate(self.installation))

    def test_current_input_invalid(self) -> None:
        installation = make_installation(
            module_type=make_module(Imp=20),
        )
        self.assertFalse(CurrentInputValidator().validate(installation))

    def test_dc_power_valid(self) -> None:
        self.assertTrue(DcPowerInverterValidator().validate(self.installation))

    def test_dc_power_invalid(self) -> None:
        installation = make_installation(module_count=20)
        self.assertFalse(DcPowerInverterValidator().validate(installation))

    def test_mppt_min_valid(self) -> None:
        self.assertTrue(MpptMinValidator().validate(self.installation))

    def test_mppt_min_invalid(self) -> None:
        installation = make_installation(module_count=1)
        self.assertFalse(MpptMinValidator().validate(installation))

    def test_mppt_max_valid(self) -> None:
        self.assertTrue(MpptMaxValidator().validate(self.installation))

    def test_mppt_max_invalid(self) -> None:
        installation = make_installation(module_count=20)
        self.assertFalse(MpptMaxValidator().validate(installation))

    def test_cold_voc_calculation_and_validation(self) -> None:
        validator = MaxInverterDcVoltageValidator()
        module = make_module()
        cold_voc = validator.calculate_cold_voc(module, DEFAULT_MIN_TEMP_C)
        self.assertGreater(cold_voc, module.voc)
        self.assertTrue(validator.validate(self.installation))

    def test_cold_voc_exceeds_inverter_limit(self) -> None:
        installation = make_installation(inverter=make_inverter(max_dc_voltage=30))
        self.assertFalse(MaxInverterDcVoltageValidator().validate(installation))

    def test_installation_checker_all_valid(self) -> None:
        self.assertTrue(InstallationChecker().check(self.installation))

    def test_installation_checker_stops_on_first_failure(self) -> None:
        installation = make_installation(module_type=make_module(Imp=99))
        self.assertFalse(InstallationChecker().check(installation))


class ClientExpectationsValidatorTests(SimpleTestCase):
    def setUp(self) -> None:
        self.installation = make_installation()
        self.requirements = make_requirements()
        self.site = make_installation_site()

    def test_max_area_valid(self) -> None:
        self.assertTrue(
            MaxAreaValidator().validate(self.installation, self.requirements, self.site)
        )

    def test_max_area_invalid(self) -> None:
        requirements = make_requirements(installation_area_m2=1.0)
        self.assertFalse(
            MaxAreaValidator().validate(self.installation, requirements, self.site)
        )

    def test_min_power_valid(self) -> None:
        self.assertTrue(
            MinPowerValidator().validate(self.installation, self.requirements, self.site)
        )

    def test_min_power_invalid(self) -> None:
        requirements = make_requirements(installation_power_kw=100.0)
        self.assertFalse(
            MinPowerValidator().validate(self.installation, requirements, self.site)
        )

    def test_max_price_valid(self) -> None:
        self.assertTrue(
            MaxPriceValidator().validate(self.installation, self.requirements, self.site)
        )

    def test_max_price_invalid(self) -> None:
        requirements = make_requirements(max_pln_budget=100.0)
        self.assertFalse(
            MaxPriceValidator().validate(self.installation, requirements, self.site)
        )

    def test_client_expectations_checker_all_valid(self) -> None:
        checker = ClientExpectationsChecker()
        self.assertTrue(
            checker.check(self.installation, self.requirements, self.site)
        )

    def test_client_expectations_checker_fails_on_budget(self) -> None:
        checker = ClientExpectationsChecker()
        requirements = make_requirements(max_pln_budget=100.0)
        self.assertFalse(checker.check(self.installation, requirements, self.site))
