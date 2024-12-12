from typing import List

from django import forms
from django.db import models
from django.utils.translation import gettext_lazy as _
from modelcluster.fields import ParentalKey
from wagtail import blocks
from wagtail.admin.panels import (
    MultiFieldPanel,
    FieldRowPanel,
    InlinePanel,
    FieldPanel,
)
from wagtail.fields import RichTextField, StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Page
from wagtail.snippets.blocks import SnippetChooserBlock
from wagtailsvg.blocks import SvgChooserBlock

from open_democracy_back.models.contents_models import Partner, Person
from open_democracy_back.utils import (
    SIMPLE_RICH_TEXT_FIELD_FEATURE,
    ManagedAssessmentType,
)


class HomePage(Page):
    # HomePage can be created only on the root
    parent_page_types = ["wagtailcore.Page"]
    preview_modes = []

    tag_line = models.CharField(
        max_length=255, default="", verbose_name=_("Phrase d'accroche")
    )
    introduction = RichTextField(
        default="",
        features=SIMPLE_RICH_TEXT_FIELD_FEATURE,
        verbose_name=_("Introduction"),
    )
    intro_image = models.ForeignKey(
        "wagtailimages.Image",
        verbose_name=_("Image"),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text=_(
            "Si l'id d'une vidéo youtube est indiqué alors l'image ne sera pas affiché sur la page d'accueil"
        ),
    )
    intro_youtube_video_id = models.CharField(
        max_length=15,
        null=True,
        blank=True,
        verbose_name=_("Vidéo Youtube (id)"),
        help_text=_(
            "Indiquer ici seulement l'id de la video youtube, celui-ci est indiqué dans l'url après 'v='. Exemple : pour https://www.youtube.com/watch?v=xMQMvVIB0vM renseigner xMQMvVIB0vM"
        ),
    )
    feedback_block_title = models.CharField(
        max_length=68,
        verbose_name=_("Titre du bloc retours d'expérience"),
        blank=True,
        help_text=_(
            "Si ce champ est vide les retours d'expérience ne s'afficheront pas sur l'accueil"
        ),
    )
    feedback_block_intro = models.TextField(
        verbose_name=_("Intro du bloc retours d'expérience"), blank=True
    )
    blog_block_title = models.CharField(
        max_length=68,
        verbose_name=_("Titre du bloc Blog"),
        blank=True,
        help_text=_(
            "Si ce champ est vide les articles de blog ne s'afficheront pas sur l'accueil"
        ),
    )
    blog_block_intro = models.TextField(verbose_name="Intro du bloc Blog", blank=True)
    resources_block_title = models.CharField(
        max_length=68,
        verbose_name=_("Titre du bloc Ressources"),
        blank=True,
        help_text=_(
            "Si ce champ est vide bloc Ressources ne s'afficheront pas sur l'accueil"
        ),
    )
    resources_block_intro = models.TextField(
        verbose_name=_("Intro du bloc Ressources"), blank=True
    )
    partner_block_title = models.CharField(
        max_length=68,
        verbose_name=_("Titre du bloc Partenaires"),
        blank=True,
        help_text=_(
            "Si ce champ est vide le bloc Partenaires ne s'afficheront pas sur l'accueil"
        ),
    )
    partner_block_intro = models.TextField(
        verbose_name=_("Intro du bloc Partenaires"), blank=True
    )

    content_panels = Page.content_panels + [
        FieldPanel("tag_line"),
        FieldPanel("introduction"),
        MultiFieldPanel(
            [
                FieldPanel("intro_image"),
                FieldPanel("intro_youtube_video_id"),
            ],
            heading=_("Image ou Vidéo d'introduction"),
        ),
        MultiFieldPanel(
            [
                FieldPanel("feedback_block_title"),
                FieldPanel("feedback_block_intro"),
            ],
            heading=_("Retour d'expérience"),
        ),
        MultiFieldPanel(
            [
                FieldPanel("blog_block_title"),
                FieldPanel("blog_block_intro"),
            ],
            heading=_("Blog"),
        ),
        MultiFieldPanel(
            [
                FieldPanel("resources_block_title"),
                FieldPanel("resources_block_intro"),
            ],
            heading=_("Ressources"),
        ),
        MultiFieldPanel(
            [
                FieldPanel("partner_block_title"),
                FieldPanel("partner_block_intro"),
            ],
            heading=_("Partenaires"),
        ),
    ]

    class Meta:
        verbose_name = _("Page d'accueil")


class UsagePage(Page):
    parent_page_types = ["HomePage"]
    subpage_types: List[str] = []
    max_count_per_parent = 1
    preview_modes = []

    tag_line = models.TextField(default="", verbose_name=_("Phrase d'accroche"))
    introduction = RichTextField(
        default="",
        features=SIMPLE_RICH_TEXT_FIELD_FEATURE,
        verbose_name=_("Introduction"),
    )
    intro_image = models.ForeignKey(
        "wagtailimages.Image",
        verbose_name=_("Image"),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    step_of_use_title = models.CharField(
        max_length=68,
        verbose_name=_("Titre"),
        blank=True,
        help_text=_(
            "Si ce champ est vide les étapes d'utilisation du DémoMètre ne s'afficheront pas"
        ),
    )
    step_of_use_intro = models.CharField(
        max_length=510, verbose_name=_("Intro"), blank=True
    )
    steps_of_use = StreamField(
        [
            (
                "step",
                blocks.StructBlock(
                    [
                        ("image", ImageChooserBlock(label=_("Image"))),
                        ("title", blocks.CharBlock(label=_("Titre"))),
                        ("description", blocks.TextBlock(label=_("Description"))),
                    ],
                    label_format=_("Étape : {title}"),
                    label=_("Étape"),
                ),
            )
        ],
        blank=True,
        verbose_name=_("Etapes d'utilisation"),
        use_json_field=True,
    )

    participate_block_title = models.CharField(
        max_length=68,
        verbose_name=_("Titre"),
        blank=True,
        help_text=_(
            "Si ce champ est vide les étapes d'utilisation du DémoMètre ne s'afficheront pas"
        ),
    )
    participate_block_intro = models.CharField(
        max_length=510, verbose_name=_("Intro"), blank=True
    )
    participate_left_paragraph = RichTextField(
        default="",
        features=SIMPLE_RICH_TEXT_FIELD_FEATURE,
        verbose_name=_("Paragraphe de gauche"),
        blank=True,
    )
    participate_right_paragraph = RichTextField(
        default="",
        features=SIMPLE_RICH_TEXT_FIELD_FEATURE,
        verbose_name=_("Paragraphe de droite"),
        blank=True,
    )

    start_assessment_block_title = models.CharField(
        max_length=68,
        verbose_name=_("Titre"),
        blank=True,
        help_text=_(
            "Si ce champ est vide les étapes d'utilisation du DémoMètre ne s'afficheront pas"
        ),
    )
    start_assessment_block_intro = models.CharField(
        max_length=510, verbose_name=_("Intro"), blank=True
    )
    start_assessment_block_data = StreamField(
        [
            (
                "assessment_type",
                blocks.StructBlock(
                    [
                        ("title", blocks.CharBlock(label=_("Titre"))),
                        (
                            "type",
                            blocks.ChoiceBlock(
                                choices=ManagedAssessmentType.choices, label=_("Type")
                            ),
                        ),
                        (
                            "pdf_button",
                            blocks.CharBlock(label=_("Nom du bouton pour le pdf")),
                        ),
                    ],
                    label_format=_("Evaluation : {title}"),
                    label=_("Type d'évaluation"),
                ),
            )
        ],
        blank=True,
        verbose_name=_("Descriptif des différents types d'évaluation"),
        help_text=_(
            "Pour modifier le descriptif de chaque type d'évaluation il faut directement aller dans le type d'évaluation correspondant"
        ),
        use_json_field=True,
    )

    # trainings
    training_block_title = models.CharField(
        verbose_name=_("Titre de la section formation"),
        max_length=100,
        blank=True,
        default=_("Formations certifiantes"),
    )
    training_block_intro = RichTextField(
        default=_(
            "Démocratie Ouverte vous propose des formations pour accompagner des évaluations DémoMètre et/ou animer des ateliers d’évaluations."
        ),
        features=SIMPLE_RICH_TEXT_FIELD_FEATURE,
        verbose_name=_("Intro de la section formation"),
        blank=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("tag_line"),
        FieldPanel("introduction"),
        FieldPanel("intro_image"),
        MultiFieldPanel(
            [
                FieldPanel("step_of_use_title"),
                FieldPanel("step_of_use_intro"),
                FieldPanel("steps_of_use", classname="full"),
            ],
            heading=_("Etapes d'utilisation du DémoMètre"),
        ),
        MultiFieldPanel(
            [
                FieldPanel("participate_block_title"),
                FieldPanel("participate_block_intro", widget=forms.Textarea),
                FieldRowPanel(
                    [
                        FieldPanel("participate_left_paragraph"),
                        FieldPanel("participate_right_paragraph"),
                    ],
                    heading=_("Description"),
                ),
            ],
            heading=_("Participer à une évaluation en cours"),
        ),
        MultiFieldPanel(
            [
                FieldPanel("start_assessment_block_title"),
                FieldPanel("start_assessment_block_intro", widget=forms.Textarea),
                FieldPanel("start_assessment_block_data", classname="full"),
            ],
            heading=_("Lancer une nouvelle évaluation"),
        ),
        MultiFieldPanel(
            [
                FieldPanel("training_block_title"),
                FieldPanel("training_block_intro"),
            ],
            heading=_("Formations"),
        ),
    ]

    class Meta:
        verbose_name = _("Page des utilisations possibles")


class ReferentialPage(Page):
    parent_page_types = ["HomePage"]
    subpage_types: List[str] = []
    max_count_per_parent = 1
    preview_modes = []

    introduction = models.TextField(default="")

    description = RichTextField(
        default="",
        features=SIMPLE_RICH_TEXT_FIELD_FEATURE,
        verbose_name=_("Description"),
    )

    rosette_legend = RichTextField(
        blank=True,
        default="",
        features=SIMPLE_RICH_TEXT_FIELD_FEATURE,
        verbose_name=_("Légende du schéma interactif"),
    )

    pillar_structure_legend = RichTextField(
        blank=True,
        default="",
        features=SIMPLE_RICH_TEXT_FIELD_FEATURE,
        verbose_name=_("Légende du schéma d'arborescence du DémoMètre"),
    )

    pillar_block_title = models.CharField(
        max_length=68,
        verbose_name=_("Titre"),
        blank=True,
        help_text=_(
            "si ce champ est vide l'explication des piliers ne s'affichera pas"
        ),
    )
    pillar_block_left_content = RichTextField(
        default="",
        blank=True,
        features=SIMPLE_RICH_TEXT_FIELD_FEATURE,
        verbose_name=_("Paragraphe de gauche"),
    )
    pillar_block_right_content = RichTextField(
        default="",
        blank=True,
        features=SIMPLE_RICH_TEXT_FIELD_FEATURE,
        verbose_name=_("Paragraphe de droite"),
    )
    pillar_block_image = models.ForeignKey(
        "wagtailimages.Image",
        verbose_name=_("Image"),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    marker_block_title = models.CharField(
        max_length=68,
        verbose_name=_("Titre"),
        blank=True,
        help_text=_(
            "si ce champ est vide l'explication des marqueurs ne s'affichera pas"
        ),
    )
    marker_block_content = RichTextField(
        default="",
        blank=True,
        features=SIMPLE_RICH_TEXT_FIELD_FEATURE,
        verbose_name=_("Contenu"),
    )

    criteria_block_title = models.CharField(
        max_length=68,
        verbose_name=_("Titre"),
        blank=True,
        help_text=_(
            "si ce champ est vide l'explication des critères d'évaluation ne s'affichera pas"
        ),
    )
    criteria_block_left_content = RichTextField(
        default="",
        blank=True,
        features=SIMPLE_RICH_TEXT_FIELD_FEATURE,
        verbose_name=_("Paragraphe de gauche"),
    )
    criteria_block_right_content = RichTextField(
        default="",
        blank=True,
        features=SIMPLE_RICH_TEXT_FIELD_FEATURE,
        verbose_name=_("Paragraphe de droite"),
    )

    content_panels = Page.content_panels + [
        FieldPanel("introduction"),
        FieldPanel("description"),
        FieldPanel("rosette_legend"),
        FieldPanel("pillar_structure_legend"),
        MultiFieldPanel(
            [
                FieldPanel("pillar_block_title"),
                FieldRowPanel(
                    [
                        FieldPanel("pillar_block_left_content"),
                        FieldPanel("pillar_block_right_content"),
                    ],
                    heading=_("Contenu"),
                ),
                FieldPanel("pillar_block_image"),
            ],
            heading=_("Explication des piliers"),
        ),
        MultiFieldPanel(
            [
                FieldPanel("marker_block_title"),
                FieldPanel("marker_block_content"),
            ],
            heading=_("Explication des marqueurs"),
        ),
        MultiFieldPanel(
            [
                FieldPanel("criteria_block_title"),
                FieldRowPanel(
                    [
                        FieldPanel("criteria_block_left_content"),
                        FieldPanel("criteria_block_right_content"),
                    ],
                    heading=_("Contenu"),
                ),
            ],
            heading=_("Explication des critères d'évaluation"),
        ),
    ]

    class Meta:
        verbose_name = _("Référentiel")


class ParticipationBoardPage(Page):
    parent_page_types = ["HomePage"]
    subpage_types: List[str] = []
    max_count_per_parent = 1
    preview_modes = []

    class Meta:
        verbose_name = _("Tableau de bord de la participation")


class ResultsPage(Page):
    parent_page_types = ["HomePage"]
    subpage_types: List[str] = []
    max_count_per_parent = 1
    preview_modes = []

    tag_line = models.CharField(max_length=510, default="", verbose_name=_("Consigne"))
    tag_line_no_results = models.CharField(
        max_length=510, default="", verbose_name=_("Consigne si aucun résultat publié")
    )
    introduction = RichTextField(
        default="",
        features=SIMPLE_RICH_TEXT_FIELD_FEATURE,
        verbose_name=_("Introduction"),
        blank=True,
    )
    intro_image = models.ForeignKey(
        "wagtailimages.Image",
        verbose_name=_("Image"),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    content_panels = Page.content_panels + [
        FieldPanel("tag_line"),
        FieldPanel("tag_line_no_results"),
        FieldPanel("introduction"),
        FieldPanel("intro_image"),
    ]

    class Meta:
        verbose_name = _("Page de résultats")


class ProjectPage(Page):
    parent_page_types = ["HomePage"]
    subpage_types: List[str] = []
    max_count_per_parent = 1
    preview_modes = []

    tag_line = models.CharField(
        max_length=510, default="", verbose_name=_("Phrase d'accroche")
    )
    introduction = RichTextField(
        default="",
        features=SIMPLE_RICH_TEXT_FIELD_FEATURE,
        verbose_name=_("Introduction"),
        blank=True,
    )
    intro_image = models.ForeignKey(
        "wagtailimages.Image",
        verbose_name=_("Image"),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    why_block_title = models.CharField(
        max_length=68,
        verbose_name=_("Titre"),
        blank=True,
        help_text=_("Si ce champ est vide le bloc ne s'affichera pas"),
    )
    why_block_data = StreamField(
        [
            (
                "richtext",
                blocks.RichTextBlock(
                    label=_("Paragraphe"),
                    features=SIMPLE_RICH_TEXT_FIELD_FEATURE,
                ),
            ),
            ("image", ImageChooserBlock(label=_("Image"))),
        ],
        blank=True,
        verbose_name="Texte",
        use_json_field=True,
    )

    objective_block_title = models.CharField(
        max_length=68,
        verbose_name=_("Titre"),
        blank=True,
        help_text=_("Si ce champ est vide le bloc ne s'affichera pas"),
    )
    objective_block_data = StreamField(
        [
            (
                "objective",
                blocks.StructBlock(
                    [
                        (
                            "svg",
                            SvgChooserBlock(
                                label=_("Icone au format svg"),
                                help_text=_(
                                    "Pour ajouter un SVG d'abord l'ajouter dans le menu SVG"
                                ),
                            ),
                        ),
                        ("title", blocks.CharBlock(label=_("Titre"))),
                    ],
                    label_format=_("Objectif : {title}"),
                    label=_("Objectif"),
                ),
            )
        ],
        blank=True,
        verbose_name=_("Les objectifs"),
        use_json_field=True,
    )

    impact_block_title = models.CharField(
        max_length=68,
        verbose_name=_("Titre"),
        blank=True,
        help_text=_("Si ce champ est vide le bloc ne s'affichera pas"),
    )
    impact_block_data = StreamField(
        [
            (
                "impact",
                blocks.StructBlock(
                    [
                        ("image", ImageChooserBlock(label=_("Image"))),
                        ("title", blocks.CharBlock(label=_("Titre"))),
                    ],
                    label_format=_("Impact : {title}"),
                    label=_("Impact"),
                ),
            )
        ],
        blank=True,
        verbose_name=_("Les impacts"),
        use_json_field=True,
    )

    who_block_title = models.CharField(
        max_length=68,
        verbose_name=_("Titre"),
        blank=True,
        help_text=_("Si ce champ est vide le bloc ne s'affichera pas"),
    )
    who_crew_sub_block_title = models.CharField(
        max_length=68,
        verbose_name=_("Equipe Démocratie Ouverte - titre"),
        blank=True,
        help_text=_("Si ce champ est vide le bloc ne s'affichera pas"),
    )
    who_crew_sub_block_image = models.ForeignKey(
        "wagtailimages.Image",
        verbose_name=_("Logo Démocratie Ouverte"),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    who_committee_sub_block_title = models.CharField(
        max_length=68,
        verbose_name=_("Le Comité d’orientation - titre"),
        blank=True,
        help_text=_("Si ce champ est vide le bloc ne s'affichera pas"),
    )
    who_committee_sub_block_description = RichTextField(
        default="",
        features=SIMPLE_RICH_TEXT_FIELD_FEATURE,
        verbose_name=_("Le Comité d’orientation - description"),
        blank=True,
    )
    who_committee_sub_block_data = StreamField(
        [
            (
                "group_committees",
                blocks.StructBlock(
                    [
                        ("committee", blocks.CharBlock(label="Nom")),
                        (
                            "committee_members",
                            blocks.ListBlock(
                                SnippetChooserBlock(Person), label="Membre"
                            ),
                        ),
                    ],
                    label_format="{title}",
                    label=_("Groupe du Comité d’orientation"),
                ),
            )
        ],
        blank=True,
        verbose_name=_("Membres du Comité - contenu"),
        use_json_field=True,
    )

    who_partner_sub_block_title = models.CharField(
        max_length=68,
        verbose_name=_("Partenaires - titre"),
        blank=True,
        help_text=_("Si ce champ est vide le bloc ne s'affichera pas"),
    )
    who_partner_sub_block_data = StreamField(
        [
            (
                "group_partners",
                blocks.StructBlock(
                    [
                        ("title", blocks.CharBlock(label=_("Titre"))),
                        ("description", blocks.CharBlock(label=_("Description"))),
                        ("partners", blocks.ListBlock(SnippetChooserBlock(Partner))),
                    ],
                    label_format="{title}",
                    label=_("Type de partenaires"),
                ),
            )
        ],
        blank=True,
        verbose_name=_("Partenaires - contenu"),
        use_json_field=True,
    )

    how_block_title = models.CharField(
        max_length=68,
        verbose_name=_("Titre"),
        blank=True,
        help_text=_("Si ce champ est vide le bloc ne s'affichera pas"),
    )
    how_block_data = StreamField(
        [
            ("title", blocks.CharBlock(label=_("Titre"))),
            (
                "richtext",
                blocks.RichTextBlock(
                    label=_("Paragraphe"),
                    features=SIMPLE_RICH_TEXT_FIELD_FEATURE,
                ),
            ),
            (
                "step",
                blocks.ListBlock(
                    blocks.StructBlock(
                        [
                            (
                                "svg",
                                SvgChooserBlock(
                                    label=_("Icone au format svg"),
                                    help_text=_(
                                        "Pour ajouter un SVG d'abord l'ajouter dans le menu SVG"
                                    ),
                                ),
                            ),
                            ("title", blocks.CharBlock(label=_("Titre"))),
                            (
                                "richtext",
                                blocks.RichTextBlock(
                                    label=_("Descriptif"),
                                    features=SIMPLE_RICH_TEXT_FIELD_FEATURE,
                                ),
                            ),
                            (
                                "link",
                                blocks.CharBlock(
                                    label=_("Lien en savoir plus"), required=False
                                ),
                            ),
                        ]
                    ),
                    label_format=_("Carte : {title}"),
                    label=_("Etapes"),
                ),
            ),
        ],
        blank=True,
        verbose_name=_("Contenu"),
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("tag_line", widget=forms.Textarea),
        FieldPanel("introduction"),
        FieldPanel("intro_image"),
        MultiFieldPanel(
            [
                FieldPanel("why_block_title"),
                FieldPanel("why_block_data", classname="full"),
            ],
            heading=_("Bloc pourquoi"),
        ),
        MultiFieldPanel(
            [
                FieldPanel("objective_block_title"),
                FieldPanel("objective_block_data", classname="full"),
            ],
            heading=_("Bloc objectif"),
        ),
        MultiFieldPanel(
            [
                FieldPanel("impact_block_title"),
                FieldPanel("impact_block_data", classname="full"),
            ],
            heading=_("Bloc Impact"),
        ),
        MultiFieldPanel(
            [
                FieldPanel("who_block_title"),
                MultiFieldPanel(
                    [
                        FieldPanel("who_crew_sub_block_title"),
                        FieldPanel("who_crew_sub_block_image"),
                        InlinePanel(
                            "who_crew_sub_block_members",
                            label=_("Membres de Démocratie Ouverte"),
                        ),
                    ],
                    heading=_("Sous bloc : Equipe Démocratie Ouverte"),
                ),
                MultiFieldPanel(
                    [
                        FieldPanel("who_committee_sub_block_title"),
                        FieldPanel("who_committee_sub_block_description"),
                        FieldPanel("who_committee_sub_block_data", classname="full"),
                    ],
                    heading=_("Sous bloc : Equipe Comité d’orientation"),
                ),
                MultiFieldPanel(
                    [
                        FieldPanel("who_partner_sub_block_title"),
                        FieldPanel("who_partner_sub_block_data", classname="full"),
                    ],
                    heading=_("Sous bloc : Partenaire"),
                ),
            ],
            heading=_("Bloc Avec Qui"),
        ),
        MultiFieldPanel(
            [
                FieldPanel("how_block_title"),
                FieldPanel("how_block_data", classname="full"),
            ],
            heading=_("Bloc comment"),
        ),
    ]

    class Meta:
        verbose_name = _("Page du projet")


class ProjectPagePerson(models.Model):
    page = ParentalKey(
        ProjectPage, on_delete=models.CASCADE, related_name="who_crew_sub_block_members"
    )
    person = models.ForeignKey(
        Person, on_delete=models.CASCADE, verbose_name=_("Membre")
    )

    panels = [
        FieldPanel("person"),
    ]

    class Meta:
        unique_together = ("page", "person")


class EvaluationInitiationPage(Page):
    parent_page_types = ["HomePage"]
    subpage_types: List[str] = []
    max_count_per_parent = 1
    preview_modes = []

    search_assessment_title = models.CharField(
        verbose_name=_("title"),
        max_length=255,
    )
    search_assessment_description = models.TextField(
        default="", verbose_name=_("Description"), blank=True
    )
    search_assessment_locality_type_question = models.TextField(
        default="",
        verbose_name=_("Question Commune / Interco"),
        blank=True,
    )
    search_assessment_locality_type_description = models.TextField(
        default="",
        verbose_name=_("Description de la question Commune / Interco"),
        blank=True,
    )
    search_assessment_zip_code_question = models.TextField(
        default="",
        verbose_name=_("Question du code postal"),
        blank=True,
    )
    search_assessment_zip_code_description = models.TextField(
        default="",
        verbose_name=_("Description de la question du code postal"),
        blank=True,
    )
    search_assessment_no_result = models.TextField(
        default="",
        verbose_name=_("Aucun résultat"),
        blank=True,
    )

    cgu_consent_title = models.CharField(
        max_length=255, default="", verbose_name=_("Titre")
    )
    cgu_consent_description_loggedin = models.TextField(
        default="",
        verbose_name=_("Description pour un utilisateur connecté"),
        blank=True,
    )
    cgu_consent_description_loggedout = models.TextField(
        default="",
        verbose_name=_("Description pour un utilisateur NON connecté"),
        blank=True,
    )

    cgv_consent_title = models.CharField(
        max_length=255, default="", verbose_name=_("Titre")
    )
    cgv_consent_description = models.TextField(
        default="",
        verbose_name=_("Description"),
        blank=True,
    )
    royalty_description = models.TextField(
        default="", verbose_name=_("Texte sur redevance d'utilisation"), blank=True
    )

    no_assessment_title = models.CharField(
        max_length=255, default="", verbose_name=_("Titre")
    )
    no_assessment_description = RichTextField(
        verbose_name=_("Description"),
        default="",
        features=SIMPLE_RICH_TEXT_FIELD_FEATURE,
        blank=True,
    )

    one_quick_assessment_title = models.CharField(
        max_length=255, default="", verbose_name=_("Titre")
    )
    one_quick_assessment_description = RichTextField(
        verbose_name=_("Description"),
        default="",
        features=SIMPLE_RICH_TEXT_FIELD_FEATURE,
        blank=True,
    )

    one_assessment_with_expert_title = models.CharField(
        max_length=255, default="", verbose_name=_("Titre")
    )
    one_assessment_with_expert_description = RichTextField(
        verbose_name=_("Description"),
        default="",
        features=SIMPLE_RICH_TEXT_FIELD_FEATURE,
        blank=True,
    )

    one_participation_assessment_title = models.CharField(
        max_length=255, default="", verbose_name=_("Titre")
    )
    one_participation_assessment_description = RichTextField(
        verbose_name=_("Description"),
        default="",
        features=SIMPLE_RICH_TEXT_FIELD_FEATURE,
        blank=True,
    )
    add_expert_title = models.CharField(
        max_length=255, default="", verbose_name=_("Ajout d'un expert - Titre")
    )
    add_expert_description = models.TextField(
        default="", verbose_name=_("Ajout d'un expert - Description"), blank=True
    )
    add_expert_button_yes = models.CharField(
        max_length=68, default="", verbose_name=_("Ajout d'un expert - Bouton OUI")
    )
    add_expert_button_no = models.CharField(
        max_length=68, default="", verbose_name=_("Ajout d'un expert - Bouton NON")
    )

    dashboard_title = models.CharField(
        max_length=255,
        default="",
        verbose_name=_("Titre"),
    )
    dashboard_description = RichTextField(
        verbose_name=_("Description"),
        default="",
        features=SIMPLE_RICH_TEXT_FIELD_FEATURE,
        blank=True,
    )

    must_be_connected_to_create_title = models.CharField(
        max_length=255, default="", verbose_name=_("Titre")
    )
    must_be_connected_to_create_description = models.TextField(
        default="", verbose_name=_("Description"), blank=True
    )

    create_quick_assessment_title = models.CharField(
        max_length=255, default="", verbose_name=_("Titre")
    )
    create_quick_assessment_description = RichTextField(
        verbose_name=_("Description"),
        default="",
        features=SIMPLE_RICH_TEXT_FIELD_FEATURE,
        blank=True,
    )

    create_participation_assessment_title = models.CharField(
        max_length=255, default="", verbose_name=_("Titre")
    )
    create_participation_assessment_description = RichTextField(
        verbose_name=_("Description"),
        default="",
        features=SIMPLE_RICH_TEXT_FIELD_FEATURE,
        blank=True,
    )

    create_assessment_with_expert_title = models.CharField(
        max_length=255, default="", verbose_name=_("Titre")
    )
    create_assessment_with_expert_description = RichTextField(
        verbose_name=_("Description"),
        default="",
        features=SIMPLE_RICH_TEXT_FIELD_FEATURE,
        blank=True,
    )
    choose_expert_text = models.CharField(
        max_length=255, default="", verbose_name=_("Choisir un expert dans la liste")
    )
    if_no_expert_text = models.CharField(
        max_length=255,
        default="",
        verbose_name=_("Si il n'y a pas mon expert, contactez-nous"),
    )

    init_title = models.CharField(max_length=255, default="", verbose_name=_("Titre"))
    init_description = RichTextField(
        verbose_name=_("Description"),
        default="",
        features=SIMPLE_RICH_TEXT_FIELD_FEATURE,
        blank=True,
    )
    initiator_name_question = models.CharField(
        max_length=255,
        verbose_name=_(
            "Enoncé de la question sur le nom de l'initateur qui sera affiché publiquement"
        ),
        default="",
    )
    initiator_name_description = models.TextField(
        verbose_name=_(
            "Description de la question sur le nom de l'initateur qui sera affiché publiquement"
        ),
        default="",
        blank=True,
    )

    representativity_title = models.TextField(
        verbose_name=_(
            "Titre - page des seuils d'acceptabilité de la représentativité"
        ),
        default="",
        help_text=_(
            "Correspond à la partie où seront posées les questions sur les seuils d'acceptabilité de la représentativité"
        ),
    )
    representativity_description = RichTextField(
        verbose_name=_(
            "Description - page des seuils d'acceptabilité de la représentativité"
        ),
        default="",
        features=SIMPLE_RICH_TEXT_FIELD_FEATURE,
        help_text=_(
            "Permet à la personne de mieux comprendre les questions sur les représentativités, et lui donne des éléments de réponse"
        ),
        blank=True,
    )

    objective_questions_title = models.CharField(
        max_length=255,
        default="",
        verbose_name=_("Titre - Répondre aux questions objectives"),
    )
    objective_questions_description = RichTextField(
        verbose_name=_("Description - Répondre aux questions objectives"),
        default="",
        features=SIMPLE_RICH_TEXT_FIELD_FEATURE,
        blank=True,
    )
    objective_questions_call_to_action = models.CharField(
        max_length=32,
        verbose_name=_("Call to action - Répondre aux questions objectives"),
        default="Commencer",
    )

    initialization_validation_title = models.CharField(
        max_length=255,
        default="",
        verbose_name=_("Titre - page de validation"),
        help_text=_("S'affichera une fois l'initialisation de l'évaluation terminée"),
    )
    initialization_validation_description = RichTextField(
        verbose_name=_("Description - page de validation"),
        default="",
        features=SIMPLE_RICH_TEXT_FIELD_FEATURE,
        blank=True,
    )
    initialization_validation_call_to_action = models.CharField(
        max_length=32,
        verbose_name=_("Call to action - page de validation"),
        default=_("Commencer l'évaluation"),
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("search_assessment_title"),
                FieldPanel("search_assessment_description"),
                FieldPanel("search_assessment_locality_type_question"),
                FieldPanel("search_assessment_locality_type_description"),
                FieldPanel("search_assessment_zip_code_question"),
                FieldPanel("search_assessment_zip_code_description"),
                FieldPanel("search_assessment_no_result"),
            ],
            heading=_("Recherche d'une évaluation"),
        ),
        MultiFieldPanel(
            [
                FieldPanel("no_assessment_title"),
                FieldPanel("no_assessment_description"),
            ],
            heading=_("Aucune évaluation ne correspond"),
        ),
        MultiFieldPanel(
            [
                FieldPanel("cgu_consent_title"),
                FieldPanel("cgu_consent_description_loggedin"),
                FieldPanel("cgu_consent_description_loggedout"),
            ],
            heading=_("Consentement aux CGU"),
        ),
        MultiFieldPanel(
            [
                FieldPanel("cgv_consent_title"),
                FieldPanel("cgv_consent_description"),
                FieldPanel("royalty_description"),
            ],
            heading=_("Consentement aux CGV"),
        ),
        MultiFieldPanel(
            [
                FieldPanel("one_quick_assessment_title"),
                FieldPanel("one_quick_assessment_description"),
            ],
            heading=_("Un diagnostic rapide correspond"),
        ),
        MultiFieldPanel(
            [
                FieldPanel("one_participation_assessment_title"),
                FieldPanel("one_participation_assessment_description"),
                FieldPanel("add_expert_title"),
                FieldPanel("add_expert_description"),
                FieldPanel("add_expert_button_yes"),
                FieldPanel("add_expert_button_no"),
            ],
            heading=_("Une évaluation participative correspond"),
        ),
        MultiFieldPanel(
            [
                FieldPanel("dashboard_title"),
                FieldPanel("dashboard_description"),
            ],
            heading=_("Tableau de bord de l'évaluation"),
        ),
        MultiFieldPanel(
            [
                FieldPanel("must_be_connected_to_create_title"),
                FieldPanel("must_be_connected_to_create_description"),
            ],
            heading=_(
                "Un utilisateur non connecté ne peut pas initaliser une évaluation"
            ),
        ),
        MultiFieldPanel(
            [
                FieldPanel("one_assessment_with_expert_title"),
                FieldPanel("one_assessment_with_expert_description"),
            ],
            heading=_("Une évaluation avec expert correspond"),
        ),
        MultiFieldPanel(
            [
                FieldPanel("create_quick_assessment_title"),
                FieldPanel("create_quick_assessment_description"),
            ],
            heading=_("Créer un diagnostic rapide"),
        ),
        MultiFieldPanel(
            [
                FieldPanel("create_participation_assessment_title"),
                FieldPanel("create_participation_assessment_description"),
            ],
            heading=_("Créer une évaluation participative"),
        ),
        MultiFieldPanel(
            [
                FieldPanel("create_assessment_with_expert_title"),
                FieldPanel("create_assessment_with_expert_description"),
                FieldPanel("choose_expert_text"),
                FieldPanel("if_no_expert_text"),
            ],
            heading=_("Créer une évaluation avec un expert"),
        ),
        MultiFieldPanel(
            [
                FieldPanel("init_title"),
                FieldPanel("init_description"),
                FieldPanel("initiator_name_question"),
                FieldPanel("initiator_name_description"),
                FieldPanel("representativity_title"),
                FieldPanel("representativity_description"),
                FieldPanel("objective_questions_title"),
                FieldPanel("objective_questions_description"),
                FieldPanel("objective_questions_call_to_action"),
                FieldPanel("initialization_validation_title"),
                FieldPanel("initialization_validation_description"),
                FieldPanel("initialization_validation_call_to_action"),
            ],
            heading=_("Initialisation de l'évaluation"),
        ),
    ]

    class Meta:
        verbose_name = _("Lancement d'une évaluation")


class EvaluationQuestionnairePage(Page):
    parent_page_types = ["HomePage"]
    subpage_types: List[str] = []
    max_count_per_parent = 1
    preview_modes = []

    role_question_title = models.CharField(
        max_length=128,
        verbose_name=_("Titre"),
        default="",
    )
    role_question_description = RichTextField(
        null=True,
        blank=True,
        features=SIMPLE_RICH_TEXT_FIELD_FEATURE,
        verbose_name=_("Description"),
    )

    end_of_profiling_title = models.CharField(
        max_length=128,
        verbose_name=_("Titre"),
        default="",
    )
    end_of_profiling_description = RichTextField(
        default="",
        features=SIMPLE_RICH_TEXT_FIELD_FEATURE,
        verbose_name=_("Description"),
        help_text=_(
            "Expliquer qu'il ne sera pas possible de revenir en arrière, puisque les questions du questionnaire dépendent du profilage"
        ),
    )
    end_of_profiling_call_to_action = models.CharField(
        max_length=32,
        verbose_name=_("Call to action"),
        default=_("Valider"),
    )

    start_title = models.CharField(
        max_length=128,
        verbose_name=_("Titre"),
    )
    start_text = models.TextField(
        verbose_name=_("Texte"),
        default="",
    )

    intermediate_step_title = models.CharField(
        max_length=128,
        verbose_name=_("Titre"),
    )
    is_intermediate_step_title_with_pillar_names = models.BooleanField(
        default=True,
        verbose_name=_("Afficher dans le titre le liste des piliers terminés"),
    )
    intermediate_step_text_logged_in = models.TextField(
        verbose_name=_("Texte pour un utilisateur connecté"),
        default="",
    )
    intermediate_step_text_logged_out = models.TextField(
        verbose_name=_("Texte pour un utilisateur non connecté"),
        default="",
    )

    finished_title = models.CharField(
        max_length=128,
        verbose_name=_("Titre"),
    )
    finished_text_logged_in = models.TextField(
        verbose_name=_("Texte pour un utilisateur connecté"),
        default="",
    )
    finished_text_logged_out = models.TextField(
        verbose_name=_("Texte pour un utilisateur non connecté"),
        default="",
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("role_question_title"),
                FieldPanel("role_question_description"),
            ],
            heading=_("Enoncé de la question concernant les rôles"),
        ),
        MultiFieldPanel(
            [
                FieldPanel("end_of_profiling_title"),
                FieldPanel("end_of_profiling_description"),
                FieldPanel("end_of_profiling_call_to_action"),
            ],
            heading=_("Page de confirmation du profilage"),
        ),
        MultiFieldPanel(
            [
                FieldPanel("start_title"),
                FieldPanel("start_text"),
            ],
            heading=_("Commencement de l'évaluation"),
        ),
        MultiFieldPanel(
            [
                FieldPanel("intermediate_step_title"),
                FieldPanel("intermediate_step_text_logged_in"),
                FieldPanel("intermediate_step_text_logged_out"),
                FieldPanel("is_intermediate_step_title_with_pillar_names"),
            ],
            heading=_(
                "Etape intermédiaire (évaluation en cours et au moins un pilier terminé)"
            ),
        ),
        MultiFieldPanel(
            [
                FieldPanel("finished_title"),
                FieldPanel("finished_text_logged_in"),
                FieldPanel("finished_text_logged_out"),
            ],
            heading=_(
                "L'Evaluation est terminée, toutes les questions ont été répondu"
            ),
        ),
    ]

    class Meta:
        verbose_name = _("Déroulement de l'évaluation")


class AnimatorPage(Page):
    parent_page_types = ["HomePage"]
    subpage_types: List[str] = []
    max_count_per_parent = 1
    preview_modes = []

    list_workshops_title = models.CharField(
        max_length=128,
        verbose_name=_("Titre"),
    )
    list_workshop_intro = models.TextField(
        verbose_name=_("Introduction"),
        default="",
    )

    close_workshop_validation = RichTextField(
        default="",
        features=SIMPLE_RICH_TEXT_FIELD_FEATURE,
        verbose_name=_("Explication du la clôture d'un workshop"),
        help_text=_(
            "Après clôture l'expert ne pourra plus accéder aux réponses des participants et donc ne pourra plus les modifier, leurs réponses seront alors pris en compte pour le calcul des résultats"
        ),
    )

    add_participants_title = models.CharField(
        max_length=128,
        verbose_name=_("Titre"),
    )
    add_participants_intro = models.TextField(
        verbose_name=_("Introduction"),
        default="",
    )

    responses_title = models.CharField(
        max_length=128,
        verbose_name=_("Titre"),
    )
    responses_intro = models.TextField(
        verbose_name=_("Introduction"),
        default="",
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("list_workshops_title"),
                FieldPanel("list_workshop_intro"),
                FieldPanel("close_workshop_validation"),
            ],
            heading=_("Page ateliers"),
        ),
        MultiFieldPanel(
            [
                FieldPanel("add_participants_title"),
                FieldPanel("add_participants_intro"),
            ],
            heading=_("Page participants"),
        ),
        MultiFieldPanel(
            [
                FieldPanel("responses_title"),
                FieldPanel("responses_intro"),
            ],
            heading=_("Page réponses"),
        ),
    ]

    class Meta:
        verbose_name = _("Espace Expert")


class ContentPage(Page):
    parent_page_types = ["HomePage"]
    subpage_types: List[str] = []
    preview_modes = []

    content = RichTextField(
        default="",
        verbose_name=_("Contenu de la page"),
    )

    content_panels = Page.content_panels + [
        FieldPanel("content"),
    ]

    class Meta:
        verbose_name = _("Page de contenu")
