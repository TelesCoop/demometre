# Generated by Django 5.0.8 on 2025-01-01 13:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "open_democracy_back",
            "0067_assessmenttype_publish_results_regardless_of_representativities",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="question",
            name="code",
            field=models.CharField(
                help_text="Correspond au numéro (ou lettre) de cette question, détermine son ordre",
                max_length=3,
                verbose_name="Code",
            ),
        ),
    ]