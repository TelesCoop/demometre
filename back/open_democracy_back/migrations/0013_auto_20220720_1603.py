# Generated by Django 3.2.11 on 2022-07-20 16:03

from django.db import migrations, models
import django.db.models.deletion
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0066_collection_management_permissions'),
        ('wagtailredirects', '0007_add_autocreate_fields'),
        ('wagtailforms', '0004_add_verbose_name_plural'),
        ('open_democracy_back', '0012_auto_20220720_0952'),
    ]

    operations = [
        migrations.CreateModel(
            name='EvaluationInitiationPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('search_assessment_title', models.CharField(max_length=255, verbose_name='title')),
                ('search_assessment_description', models.TextField(blank=True, default='', verbose_name='Description')),
                ('consent_title', models.CharField(default='', max_length=255, verbose_name='Titre')),
                ('consent_description', models.CharField(blank=True, default='', max_length=255, verbose_name='Description')),
                ('no_assessment_title', models.CharField(default='', max_length=255, verbose_name='Titre')),
                ('no_assessment_description', models.TextField(blank=True, default='', verbose_name='Description')),
                ('one_quick_assessment_title', models.CharField(default='', max_length=255, verbose_name='Titre')),
                ('one_quick_assessment_description', models.TextField(blank=True, default='', verbose_name='Description')),
                ('one_assessment_with_expert_title', models.CharField(default='', max_length=255, verbose_name='Titre')),
                ('one_assessment_with_expert_description', models.TextField(blank=True, default='', verbose_name='Description')),
                ('one_participation_assessment_title', models.CharField(default='', max_length=255, verbose_name='Titre')),
                ('one_participation_assessment_description', models.TextField(blank=True, default='', verbose_name='Description')),
                ('add_expert_title', models.CharField(default='', max_length=255, verbose_name="Ajout d'un expert - Titre")),
                ('add_expert_description', models.TextField(blank=True, default='', verbose_name="Ajout d'un expert - Description")),
                ('add_expert_button_yes', models.CharField(default='', max_length=68, verbose_name="Ajout d'un expert - Bouton OUI")),
                ('add_expert_button_no', models.CharField(default='', max_length=68, verbose_name="Ajout d'un expert - Bouton NON")),
                ('must_be_connected_to_create_title', models.CharField(default='', max_length=255, verbose_name='Titre')),
                ('must_be_connected_to_create_description', models.TextField(blank=True, default='', verbose_name='Description')),
                ('create_quick_assessment_title', models.CharField(default='', max_length=255, verbose_name='Titre')),
                ('create_quick_assessment_description', models.TextField(blank=True, default='', verbose_name='Description')),
                ('create_participation_assessment_title', models.CharField(default='', max_length=255, verbose_name='Titre')),
                ('create_participation_assessment_description', models.TextField(blank=True, default='', verbose_name='Description')),
                ('create_assessment_with_expert_title', models.CharField(default='', max_length=255, verbose_name='Titre')),
                ('create_assessment_with_expert_description', models.TextField(blank=True, default='', verbose_name='Description')),
                ('choose_expert_text', models.CharField(default='', max_length=255, verbose_name='Choisir un expert dans la liste')),
                ('if_no_expert_text', models.CharField(default='', max_length=255, verbose_name="Si il n'y a pas mon expert, contactez-nous")),
                ('init_title', models.CharField(default='', max_length=255, verbose_name='Titre')),
                ('init_description', models.TextField(blank=True, default='', verbose_name='Description')),
                ('initiator_name_question', models.CharField(default='', max_length=255, verbose_name="Enoncé de la question sur le nom de l'initateur qui sera affiché publiquement")),
                ('initiator_name_description', models.TextField(blank=True, default='', verbose_name="Description de la question sur le nom de l'initateur qui sera affiché publiquement")),
                ('representativity_title', models.TextField(default='', help_text="Correspond à la partie où seront posées les questions sur les seuils d'acceptabilité de la représentativité", verbose_name="Titre - page des seuils d'acceptabilité de la représentativité")),
                ('representativity_description', wagtail.fields.RichTextField(blank=True, default='', help_text='Permet à la personne de mieux comprendre les questions sur les représentativités, et lui donne des éléments de réponse', verbose_name="Description - page des seuils d'acceptabilité de la représentativité")),
                ('initialization_validation_title', models.CharField(default='', help_text="S'affichera une fois l'initialisation de l'évaluation terminée", max_length=255, verbose_name='Titre - page de validation')),
                ('initialization_validation_description', wagtail.fields.RichTextField(blank=True, default='', verbose_name='Description - page de validation')),
            ],
            options={
                'verbose_name': "Lancement d'une évaluation",
            },
            bases=('wagtailcore.page',),
        ),
        migrations.RemoveField(
            model_name='evaluationintropage',
            name='page_ptr',
        ),
        migrations.RemoveField(
            model_name='assessment',
            name='public_initiator',
        ),
        migrations.AlterField(
            model_name='assessment',
            name='initialized_to_the_name_of',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Initialisé au nom de'),
        ),
        migrations.AlterField(
            model_name='assessment',
            name='initiator_type',
            field=models.CharField(blank=True, choices=[('collectivity', 'La collectivité'), ('association', 'Une association'), ('individual', 'Un particulier'), ('other', 'Autre')], max_length=32, null=True),
        ),
        migrations.DeleteModel(
            name='EvaluationInitPage',
        ),
        migrations.DeleteModel(
            name='EvaluationIntroPage',
        ),
    ]