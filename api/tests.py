from typing import List, Dict, Tuple

import aiohttp
import asyncstdlib
from django.test import TestCase

from api import services


class ServiceTests(TestCase):
    """
    Test de los services.
    """

    @classmethod
    def setUpTestData(cls):
        cls.evolves_charmander: List[dict] = [{
            'evolution_details': [],
            'evolves_to': [{
                'evolution_details': [],
                'evolves_to': [],
                'is_baby': False,
                'species': {
                    'name': 'charizard',
                    'url': 'https://pokeapi.co/api/v2/pokemon-species/6/'
                }
            }],
            'is_baby': False,
            'species': {
                'name': 'charmeleon',
                'url': 'https://pokeapi.co/api/v2/pokemon-species/5/'
            }
        }]

    async def test_get_evolutions_charmander(self):
        """Prueba devolver las evoluciones."""
        evolutions_url: List[Tuple[str, str]] = [
            ('https://pokeapi.co/api/v2/pokemon-species/5/', 'charmander'),
            ('https://pokeapi.co/api/v2/pokemon-species/6/', 'charmeleon')
        ]
        async for index, evolution in asyncstdlib.enumerate(
                services.get_evolutions(self.evolves_charmander, 'charmander')):
            self.assertEqual(evolution, evolutions_url[index])

    async def test_get_detail_pokemon_charmander(self):
        """Test de los detalles del pokemon Charmander."""
        detail: Dict[str, str | int] = {
            'id': 4,
            'name': 'charmander',
            'height': 6,
            'weight': 85
        }
        endpoint: str = services.BASE_URL + "/pokemon/%s/" % 4
        async with aiohttp.ClientSession() as session:
            response = await services.get_detail_pokemon(session, endpoint)
            self.assertEqual(response['id'], detail['id'])
            self.assertEqual(response['name'], detail['name'])
            self.assertEqual(response['height'], detail['height'])
            self.assertEqual(response['weight'], detail['weight'])

    async def test_get_specie_pokemon_charmander(self):
        """Test de la obtencion de la especie del pokemon charmander."""
        pokemon_url: str = "https://pokeapi.co/api/v2/pokemon/4/"
        endpoint: str = services.BASE_URL + "/pokemon-species/%s/" % 4
        async with aiohttp.ClientSession() as session:
            async for url in services.get_specie_pokemon(session, endpoint):
                self.assertEqual(url, pokemon_url)

    async def test_get_evolution_chain_charmander(self):
        """Test para la data de evolucion de charmander."""
        detail: Dict[str, str | int | dict] = {
            'id': 2,
            'name': 'charmander',
            'url_specie': "https://pokeapi.co/api/v2/pokemon-species/4/",
            'evolves_to': {
                'name': "charmeleon",
                'url_specie': "https://pokeapi.co/api/v2/pokemon-species/5/",
                'evolves_to': {
                    'name': 'charizard',
                    'url_specie': "https://pokeapi.co/api/v2/pokemon-species/6/"
                }
            }
        }
        async with aiohttp.ClientSession() as session:
            response = await services.get_evolution_chain(session, 2)
            self.assertEqual(response['id'], detail['id'])
            self.assertEqual(
                response['chain']['species']['name'],
                detail['name']
            )
            self.assertEqual(
                response['chain']['species']['url'],
                detail['url_specie']
            )
            self.assertEqual(
                response['chain']['evolves_to'][0]['species']['name'],
                detail['evolves_to']['name']
            )
            self.assertEqual(
                response['chain']['evolves_to'][0]['species']['url'],
                detail['evolves_to']['url_specie']
            )
            self.assertEqual(
                response['chain']['evolves_to'][0]['evolves_to'][0]['species']['name'],
                detail['evolves_to']['evolves_to']['name']
            )
            self.assertEqual(
                response['chain']['evolves_to'][0]['evolves_to'][0]['species']['url'],
                detail['evolves_to']['evolves_to']['url_specie']
            )
