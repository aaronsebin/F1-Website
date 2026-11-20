
from datetime import datetime, time

from django.core.management.base import BaseCommand
from django.utils import timezone

from f1app.models import Race


RACES_2026 = [
    (1, "Australian Grand Prix", "Albert Park Grand Prix Circuit", "Australia", "2026-03-08"),
    (2, "Chinese Grand Prix", "Shanghai International Circuit", "China", "2026-03-15"),
    (3, "Japanese Grand Prix", "Suzuka International Racing Course", "Japan", "2026-03-29"),
    (4, "Miami Grand Prix", "Miami International Autodrome", "United States", "2026-05-03"),
    (5, "Canadian Grand Prix", "Circuit Gilles-Villeneuve", "Canada", "2026-05-24"),
    (6, "Monaco Grand Prix", "Circuit de Monaco", "Monaco", "2026-06-07"),
    (7, "Barcelona-Catalunya Grand Prix", "Circuit de Barcelona-Catalunya", "Spain", "2026-06-14"),
    (8, "Austrian Grand Prix", "Red Bull Ring", "Austria", "2026-06-28"),
    (9, "British Grand Prix", "Silverstone Circuit", "United Kingdom", "2026-07-05"),
    (10, "Belgian Grand Prix", "Circuit de Spa-Francorchamps", "Belgium", "2026-07-19"),
    (11, "Hungarian Grand Prix", "Hungaroring", "Hungary", "2026-07-26"),
    (12, "Dutch Grand Prix", "Circuit Zandvoort", "Netherlands", "2026-08-23"),
    (13, "Italian Grand Prix", "Autodromo Nazionale Monza", "Italy", "2026-09-06"),
    (14, "Spanish Grand Prix", "Madring", "Spain", "2026-09-13"),
    (15, "Azerbaijan Grand Prix", "Baku City Circuit", "Azerbaijan", "2026-09-26"),
    (16, "Bahrain Grand Prix in Malaysia", "Sepang International Circuit", "Malaysia", "2026-10-04"),
    (17, "Singapore Grand Prix", "Marina Bay Street Circuit", "Singapore", "2026-10-11"),
    (18, "United States Grand Prix", "Circuit of The Americas", "United States", "2026-10-25"),
    (19, "Mexico City Grand Prix", "Autodromo Hermanos Rodriguez", "Mexico", "2026-11-01"),
    (20, "São Paulo Grand Prix", "Autodromo Jose Carlos Pace", "Brazil", "2026-11-08"),
    (21, "Las Vegas Grand Prix", "Las Vegas Strip Circuit", "United States", "2026-11-21"),
    (22, "Qatar Grand Prix", "Lusail International Circuit", "Qatar", "2026-11-29"),
    (23, "Abu Dhabi Grand Prix", "Yas Marina Circuit", "United Arab Emirates", "2026-12-06"),
]


class Command(BaseCommand):
    help = "Populate the database with the 2026 Formula 1 race calendar"

    def handle(self, *args, **options):
        created_count = 0
        updated_count = 0

        current_date = timezone.localdate()

        for round_number, name, circuit, country, date_string in RACES_2026:

            race_day = datetime.strptime(
                date_string, "%Y-%m-%d"
            ).date()

            # Noon is used as a placeholder because this model
            # does not yet store the official local race start time.
            race_datetime = timezone.make_aware(
                datetime.combine(race_day, time(12, 0)),
                timezone.get_current_timezone()
            )

            status = (
                "COMPLETED"
                if race_day < current_date
                else "UPCOMING"
            )

            race, created = Race.objects.update_or_create(
                season=2026,
                round=round_number,
                defaults={
                    "race_name": name,
                    "circuit": circuit,
                    "country": country,
                    "race_date": race_datetime,
                    "status": status,
                }
            )

            if created:
                created_count += 1
            else:
                updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"2026 calendar imported successfully. "
                f"{created_count} created, {updated_count} updated."
            )
        )
