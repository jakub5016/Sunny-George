from pv_design.dto.ga_data import GAData


class GADataCache:
    _cache: GAData | None = None

    def get_cache(self) -> GAData | None:
        return GADataCache._cache

    def write_to_cache(self, data: GAData) -> None:
        if not isinstance(data, GAData):
            raise TypeError(
                f"Expected GAData, got {type(data).__name__}"
            )

        GADataCache._cache = data

    def clear_cache(self) -> None:
        GADataCache._cache = None