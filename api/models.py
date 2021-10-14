from django.contrib.postgres.fields import ArrayField
from django.db import models


class Pokemon(models.Model):
    """
    Clase que representa a un Pokemon.
    """
    id = models.PositiveBigIntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=100, null=True, unique=True)
    height = models.PositiveIntegerField(null=True)
    weight = models.PositiveIntegerField(null=True)
    base_stats = ArrayField(
        models.JSONField(null=True),
        size=6,
        null=True
    )
    evolves_from = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="evolves_to"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return f"{self.name}"

    def get_evolutions(self):
        """Devuelve las evoluciones del pokemon."""
        evolutions = self.evolves_to.annotate(
            evolution_type=models.Value("Evolution")
        ).prefetch_related('evolves_to')
        if pre_evolution := self.evolves_from:
            pre_evolution.evolution_type = "Pre-Evolution"
            return [pre_evolution, *evolutions]
        return evolutions
