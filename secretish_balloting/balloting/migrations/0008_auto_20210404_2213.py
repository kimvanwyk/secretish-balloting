import os

from django.db import migrations

from dotenv import load_dotenv

load_dotenv()


class Migration(migrations.Migration):

    dependencies = [
        ("balloting", "0007_ballot_url_summary_fragment_text"),
    ]

    def generate_superuser(apps, schema_editor):
        from django.contrib.auth.models import User

        superuser = User.objects.create_superuser(
            username=os.environ.get("ROOT_USER_USERNAME", "admin"),
            email=os.environ.get("ROOT_USER_EMAIL", ""),
            password=os.environ.get("ROOT_USER_PASSWORD"),
        )

        superuser.save()

    operations = [
        migrations.RunPython(generate_superuser),
    ]
