from celery import Task

from pv_design.services.genetic_algorithm.ga_data_cache import GADataCache


class ClearGADataCache(Task):
    name = "pv_design.tasks.clear_ga_data_cache"

    def run(self) -> None:
        GADataCache().clear_cache()
