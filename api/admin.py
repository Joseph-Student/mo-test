from django.contrib import admin

from api.models import Pokemon


@admin.register(Pokemon)
class PokemonAdmin(admin.ModelAdmin):
    """
    Administrador de los pokemon.
    """
    list_display = ("id", "name", "evolves_from")
    list_display_links = ("id", "name")
    search_fields = ("name",)
    list_select_related = ("evolves_from",)
    autocomplete_fields = ("evolves_from",)
