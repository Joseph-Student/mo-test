import asyncio

from django.core.management import BaseCommand

from api.services import get_detail_from_evolution_chain


class Command(BaseCommand):
    """
    Obtiene la informacion de los pokemon
    desde su `evolution-chain`
        • Name
        • Base stats (for the 6 categories)
        • Height
        • Weight
        • Id
        • Evolutions
    """
    help = "Obtiene y guarda la información de los pokemon desde el `evolution-chain`."

    def add_arguments(self, parser):
        """
        Agrega el id de la evolution-chain a buscar.
        """
        parser.add_argument(
            "evolution_chain_id",
            type=int,
            help="Id del evolution-chain a obtener."
        )

    def handle(self, *args, **options):
        """
        Ejecuta el comando.
        """
        pk = options['evolution_chain_id']
        try:
            pokemon: list = asyncio.run(get_detail_from_evolution_chain(pk))
        except Exception as e:
            self.stderr.write(
                self.style.ERROR(f"Ocurrió un error al obtener o guardar los datos '{e}'.")
            )
        else:
            self.stdout.write(self.style.SUCCESS("Se obtuvieron y guardaron los datos."))
            self.stdout.write(
                self.style.SUCCESS(
                    "Se guardaron los pokemon %s." %
                    ", ".join(map(str, pokemon))
                )
            )
