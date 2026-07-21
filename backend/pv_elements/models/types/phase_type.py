from django.db.models import TextChoices


class PhaseType(TextChoices):
    SINGLE = "single", "Single"
    THREE = "three", "Three"
