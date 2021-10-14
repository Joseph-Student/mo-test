# Proyecto Django de Prueba de MO Technologies.
## Back-end Technical Test
A Pokemon is a mystical creature that belongs to a fictional world, designed
and managed by the Japanese companies Nintendo, Game Freak and
Creatures. The Pokemon world is available on manga, anime adaptions, games,
retail stores and many more places.

The depth of this virtual world allows to have mountains of data only to describe
completely a Pokemon and its relations around the universe. This information is
available on the [PokeApi](https://pokeapi.co/docs/v2.html).

Develop a Django application that includes the following functionalities 
*   Build a Command that receives as its only parameter an ID, representing
the Evolution Chain. It is suggested to use the service “evolution-chains”
as a starting point (integrate as many services as needed to complete
the requirement) to fetch and store the following information:
    * Name 
    * Base stats (for the 6 categories)
    * Height 
    * Weight 
    * Id 
    * Evolutions

Expose a Web Service which only parameter is the “name” of a Pokemon
search. This service must not do a request towards the PokeApi. The
response must include the following information:
  * Pokemon details available 
  * Include for all the evolutions related 
    * Evolution type (Preevolution / Evolution)
    * Id 
    * Name

## Installation

### Prerequisites
- Python >= 3:
    - [Linux/UNIX Download](https://www.python.org/downloads/source/)
    - [Mac OS X Download](https://www.python.org/downloads/mac-osx/)
    - [Windows Download](https://www.python.org/downloads/windows/)

- PostgreSQL:
    - [Linux/Ubuntu Install](https://www.postgresql.org/download/linux/ubuntu/)
    - [Linux/Debian Install](https://www.postgresql.org/download/linux/debian/)
    - [Mac OS X Install](https://www.postgresql.org/download/macosx/)
    - [Windows Install](https://www.postgresql.org/download/windows/)
    
- Pipenv:
    - [Pipenv documentation](https://github.com/pypa/pipenv)

### Database setup
Puede configurar la base de datos mediante el siguiente comando:

```bash
psql -U postgres -W postgres
```

```postgresql
CREATE USER db_user WITH PASSWORD 'db_user_password';
CREATE DATABASE db_name WITH OWNER db_user;
```
### Install packages

Instalar las dependencias mediante Pipenv con el Pipfile.lock

```bash
pipenv sync
```

Y luego activa el entorno virtual

```bash
pipenv shell
```

### Initial Django setup

#### .env file

Además debe crear el archivo .env con las variables de entorno del proyecto

##### DJANGO SETTINGS

Environment variable | Example value | Required | Default
---|---|---|---
DJANGO_ALLOWEB_HOSTS | `*` | Yes | ``
DATABASE_URL | `postgres://USER:PASSWORD@HOST:PORT/DB_NAME?sslmode=require` | Yes | `postgres://localhost`
DJANGO_DEBUG | `off` | Yes | ``
DJANGO_SETTINGS_MODULE | `path.module.settings` | No | `config.settings.base`
DJANGO_SECRET_KEY | A Django secret key. This can be generated from https://djecrety.ir/ | Yes |

## Usage

##### Config project Django

Se deben correr las migraciones con el siguiente comando:

```bash
python manage.py migrate
```

##### Create superuser
Para crear un superusuario debe introducir el siguiente comando
```bash
python manage.py createsuperuser
Username: <username_admin>
Email address: <admin_email>
Password: <admin_password>
Password (again): <admin_password>
```

##### Run server
```bash
python manage.py runserver
```

#### Commands
Se creó el commando `getpokemon` el cual obtiene y guarda 
los siguientes datos en la base de datos:
  * Name 
  * Base stats (for the 6 categories)
  * Height 
  * Weight 
  * Id 
  * Evolutions

##### Examples
```bash
python manage.py getpokemon 5
```
```bash
'Se obtuvieron y guardaron los datos.'
'Se guardaron los pokemon weedle, kakuna, beedrill.'
```

#### Web Services
Se creó un web service alojado en el endpoint `/api/pokemon/{name}/`
el cual recibe el nombre de algún pokemon y muestra los siguientes datos:
  * Pokemon details available 
  * Include for all the evolutions related 
    * Evolution type (Pre-Evolution / Evolution)
    * Id 
    * Name

##### Examples

Hacer una consulta al endpoint:
```bash
curl http://localhost:8000/api/pokemon/kakuna/
```
El cual da como resultado el siguiente JSON:
```json
{
    "id": 14,
    "evolutions": [
        {
            "id": 13,
            "name": "weedle",
            "evolution_type": "Pre-Evolution"
        },
        {
            "id": 15,
            "name": "beedrill",
            "evolution_type": "Evolution"
        }
    ],
    "name": "kakuna",
    "height": 6,
    "weight": 100,
    "base_stats": [
        {
            "name": "hp",
            "effort": 0,
            "base_stat": 45
        },
        {
            "name": "attack",
            "effort": 0,
            "base_stat": 25
        },
        {
            "name": "defense",
            "effort": 2,
            "base_stat": 50
        },
        {
            "name": "special-attack",
            "effort": 0,
            "base_stat": 25
        },
        {
            "name": "special-defense",
            "effort": 0,
            "base_stat": 25
        },
        {
            "name": "speed",
            "effort": 0,
            "base_stat": 35
        }
    ]
}
```

#### Tests

Para correr los test se pueden ejecutar mediante Django.
```bash
python manage.py test
```

## Contributing
Contribuciones por Joseph Pérez
