
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from f1app.models import Race


IMAGE_NAMES = {
    1: "01_australian_grand_prix.png",
    2: "02_chinese_grand_prix.png",
    3: "03_japanese_grand_prix.png",
    4: "04_miami_grand_prix.png",
    5: "05_canadian_grand_prix.png",
    6: "06_monaco_grand_prix.png",
    7: "07_barcelona_catalunya_grand_prix.png",
    8: "08_austrian_grand_prix.png",
    9: "09_british_grand_prix.png",
    10: "10_belgian_grand_prix.png",
    11: "11_hungarian_grand_prix.png",
    12: "12_dutch_grand_prix.png",
    13: "13_italian_grand_prix.png",
    14: "14_spanish_grand_prix.png",
    15: "15_azerbaijan_grand_prix.png",
    16: "16_bahrain_grand_prix_malaysia.png",
    17: "17_singapore_grand_prix.png",
    18: "18_united_states_grand_prix.png",
    19: "19_mexico_city_grand_prix.png",
    20: "20_sao_paulo_grand_prix.png",
    21: "21_las_vegas_grand_prix.png",
    22: "22_qatar_grand_prix.png",
    23: "23_abu_dhabi_grand_prix.png",
}


class Command(BaseCommand):
    help = "Link circuit images to 2026 race records"

    def handle(self, *args, **options):
        image_folder = Path(settings.MEDIA_ROOT) / "circuits"

        linked = 0
        missing = 0

        for round_number, filename in IMAGE_NAMES.items():
            image_path = image_folder / filename

            race = Race.objects.filter(
                season=2026,
                round=round_number
            ).first()

            if not race:
                self.stdout.write(
                    self.style.WARNING(
                        f"Round {round_number}: Race record not found."
                    )
                )
                missing += 1
                continue

            if not image_path.is_file():
                self.stdout.write(
                    self.style.WARNING(
                        f"Missing image: {filename}"
                    )
                )
                missing += 1
                continue

            race.circuit_image.name = f"circuits/{filename}"
            race.save(update_fields=["circuit_image"])

            self.stdout.write(
                self.style.SUCCESS(
                    f"Linked: {race.race_name}"
                )
            )
            linked += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Finished: {linked} linked, {missing} missing."
            )
        )
