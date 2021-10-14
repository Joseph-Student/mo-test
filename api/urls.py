"""
Urls de la app `api`.
"""
from rest_framework.routers import DefaultRouter

from api.views import PokemonDetailViewSet

router = DefaultRouter()
router.register(r'pokemon', PokemonDetailViewSet)
