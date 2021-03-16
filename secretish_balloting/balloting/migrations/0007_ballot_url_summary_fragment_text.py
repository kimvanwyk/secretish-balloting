# Generated by Django 3.1.7 on 2021-03-16 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("balloting", "0006_auto_20210314_1619"),
    ]

    operations = [
        migrations.AddField(
            model_name="ballot",
            name="url_summary_fragment_text",
            field=models.CharField(
                default="48245591",
                help_text="Slug text to be used in the summary url for this ballot",
                max_length=40,
            ),
            preserve_default=False,
        ),
    ]