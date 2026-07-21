from dataclasses import dataclass
from typing import Optional

from rest_framework.request import Request


@dataclass
class InverterFiltersDTO:
    search: Optional[str]
    phases: Optional[str]
    power_min: Optional[float]
    power_max: Optional[float]
    price_min: Optional[float]
    price_max: Optional[float]

    @classmethod
    def from_request(cls, request: Request) -> "InverterFiltersDTO":
        params = request.query_params
        return cls(
            search=params.get("search") or None,
            phases=params.get("phases") or None,
            power_min=float(raw) if (raw := params.get("power_min")) else None,
            power_max=float(raw) if (raw := params.get("power_max")) else None,
            price_min=float(raw) if (raw := params.get("price_min")) else None,
            price_max=float(raw) if (raw := params.get("price_max")) else None,
        )
