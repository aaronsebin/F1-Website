
from django.core.management.base import BaseCommand
from f1app.models import Driver


DRIVERS_2026 = [
    {
        "driver_id": "norris",
        "name": "Lando",
        "surname": "Norris",
        "team": "McLaren",
        "nationality": "United Kingdom",
        "number": 1,
        "short_name": "NOR",
        "profile_url": "https://www.formula1.com/en/drivers/lando-norris",
    },
    {
        "driver_id": "piastri",
        "name": "Oscar",
        "surname": "Piastri",
        "team": "McLaren",
        "nationality": "Australia",
        "number": 81,
        "short_name": "PIA",
        "profile_url": "https://www.formula1.com/en/drivers/oscar-piastri",
    },
    {
        "driver_id": "russell",
        "name": "George",
        "surname": "Russell",
        "team": "Mercedes",
        "nationality": "United Kingdom",
        "number": 63,
        "short_name": "RUS",
        "profile_url": "https://www.formula1.com/en/drivers/george-russell",
    },
    {
        "driver_id": "antonelli",
        "name": "Andrea Kimi",
        "surname": "Antonelli",
        "team": "Mercedes",
        "nationality": "Italy",
        "number": 12,
        "short_name": "ANT",
        "profile_url": "https://www.formula1.com/en/drivers/kimi-antonelli",
    },
    {
        "driver_id": "max-verstappen",
        "name": "Max",
        "surname": "Verstappen",
        "team": "Red Bull Racing",
        "nationality": "Netherlands",
        "number": 3,
        "short_name": "VER",
        "profile_url": "https://www.formula1.com/en/drivers/max-verstappen",
    },
    {
        "driver_id": "hadjar",
        "name": "Isack",
        "surname": "Hadjar",
        "team": "Red Bull Racing",
        "nationality": "France",
        "number": 6,
        "short_name": "HAD",
        "profile_url": "https://www.formula1.com/en/drivers/isack-hadjar",
    },
    {
        "driver_id": "leclerc",
        "name": "Charles",
        "surname": "Leclerc",
        "team": "Ferrari",
        "nationality": "Monaco",
        "number": 16,
        "short_name": "LEC",
        "profile_url": "https://www.formula1.com/en/drivers/charles-leclerc",
    },
    {
        "driver_id": "hamilton",
        "name": "Lewis",
        "surname": "Hamilton",
        "team": "Ferrari",
        "nationality": "United Kingdom",
        "number": 44,
        "short_name": "HAM",
        "profile_url": "https://www.formula1.com/en/drivers/lewis-hamilton",
    },
    {
        "driver_id": "albon",
        "name": "Alexander",
        "surname": "Albon",
        "team": "Williams",
        "nationality": "Thailand",
        "number": 23,
        "short_name": "ALB",
        "profile_url": "https://www.formula1.com/en/drivers/alexander-albon",
    },
    {
        "driver_id": "sainz",
        "name": "Carlos",
        "surname": "Sainz",
        "team": "Williams",
        "nationality": "Spain",
        "number": 55,
        "short_name": "SAI",
        "profile_url": "https://www.formula1.com/en/drivers/carlos-sainz",
    },
    {
        "driver_id": "lawson",
        "name": "Liam",
        "surname": "Lawson",
        "team": "Racing Bulls",
        "nationality": "New Zealand",
        "number": 30,
        "short_name": "LAW",
        "profile_url": "https://www.formula1.com/en/drivers/liam-lawson",
    },
    {
        "driver_id": "lindblad",
        "name": "Arvid",
        "surname": "Lindblad",
        "team": "Racing Bulls",
        "nationality": "United Kingdom",
        "number": 41,
        "short_name": "LIN",
        "profile_url": "https://www.formula1.com/en/drivers/arvid-lindblad",
    },
    {
        "driver_id": "alonso",
        "name": "Fernando",
        "surname": "Alonso",
        "team": "Aston Martin",
        "nationality": "Spain",
        "number": 14,
        "short_name": "ALO",
        "profile_url": "https://www.formula1.com/en/drivers/fernando-alonso",
    },
    {
        "driver_id": "stroll",
        "name": "Lance",
        "surname": "Stroll",
        "team": "Aston Martin",
        "nationality": "Canada",
        "number": 18,
        "short_name": "STR",
        "profile_url": "https://www.formula1.com/en/drivers/lance-stroll",
    },
    {
        "driver_id": "ocon",
        "name": "Esteban",
        "surname": "Ocon",
        "team": "Haas",
        "nationality": "France",
        "number": 31,
        "short_name": "OCO",
        "profile_url": "https://www.formula1.com/en/drivers/esteban-ocon",
    },
    {
        "driver_id": "bearman",
        "name": "Oliver",
        "surname": "Bearman",
        "team": "Haas",
        "nationality": "United Kingdom",
        "number": 87,
        "short_name": "BEA",
        "profile_url": "https://www.formula1.com/en/drivers/oliver-bearman",
    },
    {
        "driver_id": "hulkenberg",
        "name": "Nico",
        "surname": "Hülkenberg",
        "team": "Audi",
        "nationality": "Germany",
        "number": 27,
        "short_name": "HUL",
        "profile_url": "https://www.formula1.com/en/drivers/nico-hulkenberg",
    },
    {
        "driver_id": "bortoleto",
        "name": "Gabriel",
        "surname": "Bortoleto",
        "team": "Audi",
        "nationality": "Brazil",
        "number": 5,
        "short_name": "BOR",
        "profile_url": "https://www.formula1.com/en/drivers/gabriel-bortoleto",
    },
    {
        "driver_id": "gasly",
        "name": "Pierre",
        "surname": "Gasly",
        "team": "Alpine",
        "nationality": "France",
        "number": 10,
        "short_name": "GAS",
        "profile_url": "https://www.formula1.com/en/drivers/pierre-gasly",
    },
    {
        "driver_id": "colapinto",
        "name": "Franco",
        "surname": "Colapinto",
        "team": "Alpine",
        "nationality": "Argentina",
        "number": 43,
        "short_name": "COL",
        "profile_url": "https://www.formula1.com/en/drivers/franco-colapinto",
    },
    {
        "driver_id": "perez",
        "name": "Sergio",
        "surname": "Pérez",
        "team": "Cadillac",
        "nationality": "Mexico",
        "number": 11,
        "short_name": "PER",
        "profile_url": "https://www.formula1.com/en/drivers/sergio-perez",
    },
    {
        "driver_id": "bottas",
        "name": "Valtteri",
        "surname": "Bottas",
        "team": "Cadillac",
        "nationality": "Finland",
        "number": 77,
        "short_name": "BOT",
        "profile_url": "https://www.formula1.com/en/drivers/valtteri-bottas",
    },
]


class Command(BaseCommand):
    help = "Populate the database with the 2026 Formula 1 driver grid"

    def handle(self, *args, **options):

        # Mark existing drivers inactive first
        Driver.objects.update(is_active=False)

        # Add or update the 2026 drivers
        for driver_data in DRIVERS_2026:
            Driver.objects.update_or_create(
                driver_id=driver_data["driver_id"],
                defaults={
                    **driver_data,
                    "is_active": True,
                    "points": 0,
                },
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully added {len(DRIVERS_2026)} drivers for the 2026 season."
            )
        )
