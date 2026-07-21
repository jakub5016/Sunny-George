from dataclasses import dataclass
from typing import Optional

from rest_framework.request import Request


@dataclass
class ModuleFiltersDTO:
    search: Optional[str]
    power_min: Optional[float]
    power_max: Optional[float]
    efficiency_min: Optional[float]
    efficiency_max: Optional[float]
    price_min: Optional[float]
    price_max: Optional[float]

    @classmethod
    def from_request(cls, request: Request) -> "ModuleFiltersDTO":
        params = request.query_params
        return cls(
            search=params.get("search") or None,
            power_min=float(raw) if (raw := params.get("power_min")) else None,
            power_max=float(raw) if (raw := params.get("power_max")) else None,
            efficiency_min=float(raw) if (raw := params.get("efficiency_min")) else None,
            efficiency_max=float(raw) if (raw := params.get("efficiency_max")) else None,
            price_min=float(raw) if (raw := params.get("price_min")) else None,
            price_max=float(raw) if (raw := params.get("price_max")) else None,
        )
