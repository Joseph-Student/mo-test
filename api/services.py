"""
Servicios externos.
"""
import logging
from typing import Optional, List

import aiohttp
from asgiref.sync import sync_to_async

from .models import Pokemon
from .utils import get

BASE_URL: str = "https://pokeapi.co/api/v2"

logger: logging.Logger = logging.getLogger("services")


async def get_evolution_chain(session: aiohttp.ClientSession, pk: int):
    async with session.get(f"{BASE_URL}/evolution-chain/{pk}/") as response:
        data: dict = await response.json()
        logger.debug("Data: %s", data)
        return data


async def get_specie_pokemon(session: aiohttp.ClientSession, url: str, default: bool = True):
    """
    Busca la url del pokemon para extraer sus detalles.
    """
    data: dict = await get(session, url)
    logger.debug("Get Specie Pokemon: %s", data)
    for variety in data['varieties']:
        if default:
            if variety['is_default']:
                yield variety['pokemon']['url']
        else:
            yield variety['pokemon']['url']


async def get_detail_pokemon(session: aiohttp.ClientSession, url: str):
    """
    Devuelve los detalles de un pokemon.
    """
    return await get(session, url)


async def get_evolutions(evolves_to: list, parent: str):
    """
    Devuelve los detalles de las evoluciones.
    """
    for evl in evolves_to:
        yield evl['species']['url'], parent

        async for evo in get_evolutions(evl['evolves_to'], evl['species']['name']):
            yield evo


def add_pokemon(data: dict, evolves_from: Optional[Pokemon] = None):
    """
    Crea un pokemon.
    """
    logger.debug("Crear un pokemon...")
    pokemon, _ = Pokemon.objects.get_or_create(
        id=data['id'],
        name=data['name'],
        defaults={
            'height': data['height'],
            'weight': data['weight'],
            'base_stats': [{
                'name': s['stat']['name'],
                'base_stat': s['base_stat'],
                'effort': s['effort']
            } for s in data['stats']],
            'evolves_from': evolves_from
        }
    )
    logger.info("Pokemon %s creado.", pokemon.name)
    return pokemon


async def get_detail_from_evolution_chain(pk: int) -> List[Pokemon]:
    """
    Obtiene los datos de los pokemon desde una evolution-chain.
    """
    async with aiohttp.ClientSession() as session:
        evolution_chain: dict = await get_evolution_chain(session, pk)
        specie_primary: str = evolution_chain['chain']['species']['url']
        evolves: list = evolution_chain['chain']['evolves_to']
        pokemon_name: str = evolution_chain['chain']['species']['name']
        pokemon_adding: List[Pokemon] = []
        pokemon_base: Optional[Pokemon] = None

        async for pokemon_url in get_specie_pokemon(session, specie_primary):
            data: dict = await get_detail_pokemon(session, pokemon_url)
            logger.info("Detail Pokemon...")
            logger.info(f"Pokemon: {data['name']}")
            logger.debug("Info: %s", data)
            pokemon_base = await sync_to_async(add_pokemon, thread_sensitive=True)(data)
            pokemon_adding.append(pokemon_base)

        pokemon_parent: Optional[Pokemon] = pokemon_base
        async for pokemon_specie_url, name in get_evolutions(evolves, pokemon_name):
            async for pokemon_url in get_specie_pokemon(session, pokemon_specie_url):
                pokemon: dict = await get_detail_pokemon(session, pokemon_url)
                logger.info(f"Evolutions of {name}...")
                logger.info(f"Pokemon {pokemon['name']}")
                logger.debug("Info: %s", pokemon)
                if name != pokemon_parent.name:
                    pokemon_parent = await sync_to_async(
                        lambda n: Pokemon.objects.filter(name=n).first()
                    )(name)
                pokemon_adding.append(
                    await sync_to_async(add_pokemon, thread_sensitive=True)(pokemon, pokemon_parent)
                )

        return pokemon_adding
