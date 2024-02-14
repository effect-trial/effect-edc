# Generated by Django 5.0 on 2023-12-21 03:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "edc_action_item",
            "0035_alter_actionitem_options_alter_actiontype_options_and_more",
        ),
        ("effect_consent", "0009_alter_subjectreconsent_options"),
        ("sites", "0002_alter_domain_unique"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="subjectconsent",
            options={
                "default_manager_name": "objects",
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
                "verbose_name": "Subject Consent",
                "verbose_name_plural": "Subject Consents",
            },
        ),
        migrations.AlterModelOptions(
            name="subjectreconsent",
            options={
                "default_manager_name": "objects",
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
                "verbose_name": "Subject re-consent",
            },
        ),
        migrations.RemoveIndex(
            model_name="subjectconsent",
            name="effect_cons_subject_867fc2_idx",
        ),
        migrations.AddField(
            model_name="historicalsubjectconsent",
            name="locale_created",
            field=models.CharField(
                blank=True,
                help_text="Auto-updated by Modeladmin",
                max_length=10,
                null=True,
                verbose_name="Locale created",
            ),
        ),
        migrations.AddField(
            model_name="historicalsubjectconsent",
            name="locale_modified",
            field=models.CharField(
                blank=True,
                help_text="Auto-updated by Modeladmin",
                max_length=10,
                null=True,
                verbose_name="Locale modified",
            ),
        ),
        migrations.AddField(
            model_name="historicalsubjectreconsent",
            name="locale_created",
            field=models.CharField(
                blank=True,
                help_text="Auto-updated by Modeladmin",
                max_length=10,
                null=True,
                verbose_name="Locale created",
            ),
        ),
        migrations.AddField(
            model_name="historicalsubjectreconsent",
            name="locale_modified",
            field=models.CharField(
                blank=True,
                help_text="Auto-updated by Modeladmin",
                max_length=10,
                null=True,
                verbose_name="Locale modified",
            ),
        ),
        migrations.AddField(
            model_name="subjectconsent",
            name="locale_created",
            field=models.CharField(
                blank=True,
                help_text="Auto-updated by Modeladmin",
                max_length=10,
                null=True,
                verbose_name="Locale created",
            ),
        ),
        migrations.AddField(
            model_name="subjectconsent",
            name="locale_modified",
            field=models.CharField(
                blank=True,
                help_text="Auto-updated by Modeladmin",
                max_length=10,
                null=True,
                verbose_name="Locale modified",
            ),
        ),
        migrations.AddField(
            model_name="subjectreconsent",
            name="locale_created",
            field=models.CharField(
                blank=True,
                help_text="Auto-updated by Modeladmin",
                max_length=10,
                null=True,
                verbose_name="Locale created",
            ),
        ),
        migrations.AddField(
            model_name="subjectreconsent",
            name="locale_modified",
            field=models.CharField(
                blank=True,
                help_text="Auto-updated by Modeladmin",
                max_length=10,
                null=True,
                verbose_name="Locale modified",
            ),
        ),
        migrations.AddIndex(
            model_name="subjectconsent",
            index=models.Index(
                fields=["modified", "created"], name="effect_cons_modifie_0d880c_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="subjectconsent",
            index=models.Index(
                fields=["user_modified", "user_created"],
                name="effect_cons_user_mo_d91f89_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="subjectreconsent",
            index=models.Index(
                fields=["modified", "created"], name="effect_cons_modifie_891b07_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="subjectreconsent",
            index=models.Index(
                fields=["user_modified", "user_created"],
                name="effect_cons_user_mo_ddf3ae_idx",
            ),
        ),
        migrations.AddConstraint(
            model_name="subjectconsent",
            constraint=models.UniqueConstraint(
                fields=("first_name", "dob", "initials", "version"),
                name="effect_consent_subjectconsent_first_uniq",
            ),
        ),
        migrations.AddConstraint(
            model_name="subjectconsent",
            constraint=models.UniqueConstraint(
                fields=(
                    "subject_identifier",
                    "first_name",
                    "dob",
                    "initials",
                    "version",
                ),
                name="effect_consent_subjectconsent_subject_uniq",
            ),
        ),
        migrations.AddConstraint(
            model_name="subjectconsent",
            constraint=models.UniqueConstraint(
                fields=("version", "subject_identifier"),
                name="effect_consent_subjectconsent_version_uniq",
            ),
        ),
    ]