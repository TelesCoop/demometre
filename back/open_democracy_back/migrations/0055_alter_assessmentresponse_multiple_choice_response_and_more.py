# Generated by Django 5.0.6 on 2024-06-24 09:00

import django.db.models.deletion
import taggit.managers
import wagtail.models.media
import wagtail.search.index
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("open_democracy_back", "0054_auto_20240419_0858"),
        (
            "taggit",
            "0006_rename_taggeditem_content_type_object_id_taggit_tagg_content_8fc721_idx",
        ),
        ("wagtailcore", "0093_uploadedfile"),
    ]

    operations = [
        migrations.AlterField(
            model_name="assessmentresponse",
            name="multiple_choice_response",
            field=models.ManyToManyField(
                related_name="multiple_choice_%(class)ss",
                to="open_democracy_back.responsechoice",
            ),
        ),
        migrations.AlterField(
            model_name="assessmentresponse",
            name="question",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="%(class)ss",
                to="open_democracy_back.question",
            ),
        ),
        migrations.AlterField(
            model_name="assessmentresponse",
            name="unique_choice_response",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="unique_choice_%(class)ss",
                to="open_democracy_back.responsechoice",
            ),
        ),
        migrations.AlterField(
            model_name="blogpost",
            name="pillars",
            field=models.ManyToManyField(
                blank=True,
                related_name="%(class)ss",
                to="open_democracy_back.pillar",
                verbose_name="Piliers concernés",
            ),
        ),
        migrations.AlterField(
            model_name="participationresponse",
            name="multiple_choice_response",
            field=models.ManyToManyField(
                related_name="multiple_choice_%(class)ss",
                to="open_democracy_back.responsechoice",
            ),
        ),
        migrations.AlterField(
            model_name="participationresponse",
            name="question",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="%(class)ss",
                to="open_democracy_back.question",
            ),
        ),
        migrations.AlterField(
            model_name="participationresponse",
            name="unique_choice_response",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="unique_choice_%(class)ss",
                to="open_democracy_back.responsechoice",
            ),
        ),
        migrations.AlterField(
            model_name="profiledefinition",
            name="conditional_question",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="%(class)s_that_depend_on_me",
                to="open_democracy_back.question",
                verbose_name="Filtre par question",
            ),
        ),
        migrations.AlterField(
            model_name="questionrule",
            name="conditional_question",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="%(class)s_that_depend_on_me",
                to="open_democracy_back.question",
                verbose_name="Filtre par question",
            ),
        ),
        migrations.AlterField(
            model_name="resource",
            name="pillars",
            field=models.ManyToManyField(
                blank=True,
                related_name="%(class)ss",
                to="open_democracy_back.pillar",
                verbose_name="Piliers concernés",
            ),
        ),
        migrations.AlterField(
            model_name="thematictag",
            name="slug",
            field=models.SlugField(
                allow_unicode=True, max_length=100, unique=True, verbose_name="slug"
            ),
        ),
    ]