import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
django.setup()

from django.core.management import call_command

with open("data.json", "w", encoding="utf-8") as f:
    call_command(
        "dumpdata",
        "--natural-foreign",
        "--natural-primary",
        indent=2,
        stdout=f,
    )

print("Done!")