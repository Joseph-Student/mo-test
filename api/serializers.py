"""
Serializadores de la app api.
"""
from rest_framework import serializers

from api.models import Pokemon


class EvolutionSerializer(serializers.ModelSerializer):
    """
    Serializador de las evoluciones de :model:`Pokemon`.
    """
    evolution_type = serializers.CharField(read_only=True)

    class Meta:
        model = Pokemon
        fields = ['id', 'name', 'evolution_type']


class PokemonSerializer(serializers.ModelSerializer):
    """
    Serializador del modelo :model:`api.Pokemon`.
    """
    evolutions = EvolutionSerializer(many=True, source="get_evolutions")

    class Meta:
        model = Pokemon
        exclude = ['evolves_from', 'created_at']
