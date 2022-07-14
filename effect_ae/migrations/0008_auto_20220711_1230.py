# Generated by Django 3.2.13 on 2022-07-11 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('effect_ae', '0007_auto_20220516_1759'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='historicalaefollowup',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical AE Follow-up Report', 'verbose_name_plural': 'historical AE Follow-up Reports'},
        ),
        migrations.AlterModelOptions(
            name='historicalaeinitial',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical AE Initial Report', 'verbose_name_plural': 'historical AE Initial Reports'},
        ),
        migrations.AlterModelOptions(
            name='historicalaesusar',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical AE SUSAR Report', 'verbose_name_plural': 'historical AE SUSAR Reports'},
        ),
        migrations.AlterModelOptions(
            name='historicalaetmg',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical AE TMG Report', 'verbose_name_plural': 'historical AE TMG Reports'},
        ),
        migrations.AlterModelOptions(
            name='historicaldeathreport',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical Death Report', 'verbose_name_plural': 'historical Death Reports'},
        ),
        migrations.AlterModelOptions(
            name='historicaldeathreporttmg',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical Death Report TMG (1st)', 'verbose_name_plural': 'historical Death Report TMG (1st)'},
        ),
        migrations.AlterModelOptions(
            name='historicaldeathreporttmgsecond',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical Death Report TMG (2nd)', 'verbose_name_plural': 'historical Death Report TMG (2nd)'},
        ),
        migrations.AlterField(
            model_name='historicalaefollowup',
            name='history_date',
            field=models.DateTimeField(db_index=True),
        ),
        migrations.AlterField(
            model_name='historicalaeinitial',
            name='history_date',
            field=models.DateTimeField(db_index=True),
        ),
        migrations.AlterField(
            model_name='historicalaesusar',
            name='history_date',
            field=models.DateTimeField(db_index=True),
        ),
        migrations.AlterField(
            model_name='historicalaetmg',
            name='history_date',
            field=models.DateTimeField(db_index=True),
        ),
        migrations.AlterField(
            model_name='historicaldeathreport',
            name='history_date',
            field=models.DateTimeField(db_index=True),
        ),
        migrations.AlterField(
            model_name='historicaldeathreporttmg',
            name='history_date',
            field=models.DateTimeField(db_index=True),
        ),
        migrations.AlterField(
            model_name='historicaldeathreporttmgsecond',
            name='history_date',
            field=models.DateTimeField(db_index=True),
        ),
    ]