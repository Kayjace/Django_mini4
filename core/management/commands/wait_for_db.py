import time

from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError
from psycopg2 import OperationalError as Psycopg2OpError


class Command(BaseCommand):
    help = "Django command to wait for the database to be available"

    def handle(self, *args, **options):
        self.stdout.write("Waiting for database...")

        for attempt in range(10):
            try:
                connection = connections["default"]
                connection.ensure_connection()  # Ensure the connection is established
                self.stdout.write(self.style.SUCCESS("PostgreSQL Database available!"))
                return  # Exit if the connection is successful
            except (Psycopg2OpError, OperationalError):
                self.stdout.write(
                    self.style.WARNING(
                        f"Database unavailable, waiting... (Attempt {attempt + 1}/10)"
                    )
                )
                time.sleep(1)

        self.stdout.write(
            self.style.ERROR("PostgreSQL Connection Failed after 10 attempts!")
        )
        exit(1)
