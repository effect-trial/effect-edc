# Generated by Django 3.2.11 on 2022-03-30 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('effect_lists', '0007_auto_20220330_1707'),
        ('effect_screening', '0013_auto_20220329_1818'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalsubjectscreening',
            name='meningitis_symptoms',
        ),
        migrations.RemoveField(
            model_name='subjectscreening',
            name='meningitis_symptoms',
        ),
        migrations.AddField(
            model_name='historicalsubjectscreening',
            name='mg_ssx_other',
            field=models.TextField(blank=True, help_text='If more than one, please separate each with a comma (,).', null=True, verbose_name="If 'Other' please specify ..."),
        ),
        migrations.AddField(
            model_name='historicalsubjectscreening',
            name='mg_ssx_since_crag',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No'), ('not_answered', 'Not answered')], default='not_answered', max_length=25, verbose_name='Has the patient had clinical signs/symptoms (SSX) of symptomatic meningitis at any time since CrAg screening?'),
        ),
        migrations.AddField(
            model_name='subjectscreening',
            name='mg_ssx',
            field=models.ManyToManyField(blank=True, to='effect_lists.SiSxMeningitis', verbose_name='If YES, specify the clinical SSX of symptomatic meningitis?'),
        ),
        migrations.AddField(
            model_name='subjectscreening',
            name='mg_ssx_other',
            field=models.TextField(blank=True, help_text='If more than one, please separate each with a comma (,).', null=True, verbose_name="If 'Other' please specify ..."),
        ),
        migrations.AddField(
            model_name='subjectscreening',
            name='mg_ssx_since_crag',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No'), ('not_answered', 'Not answered')], default='not_answered', max_length=25, verbose_name='Has the patient had clinical signs/symptoms (SSX) of symptomatic meningitis at any time since CrAg screening?'),
        ),
    ]
