from rest_framework.mixins import RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

from api.models import Pokemon
from api.serializers import PokemonSerializer


class PokemonDetailViewSet(RetrieveModelMixin, GenericViewSet):
    """
    Endpoint que devuelve el detalle de algun pokemon por su nombre.
    """
    serializer_class = PokemonSerializer
    queryset = Pokemon.objects.all()
    lookup_field = "name"
