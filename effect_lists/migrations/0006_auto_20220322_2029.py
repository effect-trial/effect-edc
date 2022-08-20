# Generated by Django 3.2.8 on 2022-03-22 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("effect_lists", "0005_delete_rankinscore"),
    ]

    operations = [
        migrations.CreateModel(
            name="Medication",
            fields=[
                (
                    "name",
                    models.CharField(
                        db_index=True,
                        help_text="This is the stored value, required",
                        max_length=250,
                        unique=True,
                        verbose_name="Stored value",
                    ),
                ),
                (
                    "display_name",
                    models.CharField(
                        db_index=True,
                        help_text="(suggest 40 characters max.)",
                        max_length=250,
                        unique=True,
                        verbose_name="Name",
                    ),
                ),
                (
                    "display_index",
                    models.IntegerField(
                        db_index=True,
                        default=0,
                        help_text="Index to control display order if not alphabetical, not required",
                        verbose_name="display index",
                    ),
                ),
                (
                    "field_name",
                    models.CharField(
                        blank=True,
                        editable=False,
                        help_text="Not required",
                        max_length=25,
                        null=True,
                    ),
                ),
                ("version", models.CharField(default="1.0", editable=False, max_length=35)),
                ("id", models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                "verbose_name": "Medication",
                "verbose_name_plural": "Medication",
                "ordering": ["display_index", "display_name"],
                "abstract": False,
                "default_permissions": ("add", "change", "delete", "view", "export", "import"),
            },
        ),
        migrations.AddIndex(
            model_name="medication",
            index=models.Index(
                fields=["id", "display_name", "display_index"],
                name="effect_list_id_9557c7_idx",
            ),
        ),
    ]
