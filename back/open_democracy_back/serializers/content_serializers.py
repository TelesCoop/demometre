from rest_framework import serializers

from open_democracy_back.models.contents_models import (
    Article,
    BlogPost,
    Feedback,
    Partner,
    Person,
    Resource,
)
from open_democracy_back.serializers.block_serializers import (
    SerializerStreamField,
    DocumentSerializer,
    RichTextSerializer,
    ImageSerializer,
)
from open_democracy_back.serializers.questionnaire_and_profiling_serializers import (
    SerializerWithTranslatedFields,
)


class FeedbackSerializer(SerializerWithTranslatedFields):
    picture_url = serializers.SerializerMethodField()

    @staticmethod
    def get_picture_url(obj: Feedback):
        if obj.picture:
            return obj.picture.file.url
        return None

    class Meta:
        model = Feedback
        fields = [
            "id",
            "person_name",
            "picture_url",
            "person_context",
            "quote",
            "external_link",
            "publish",
        ]


ARTICLE_FIELDS = [
    "id",
    "title",
    "slug",
    "publication_date",
    "content",
    "short_description",
    "image_url",
    "external_link",
    "pillars",
]


class ArticleSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    content = SerializerStreamField(
        serializers={
            "image": ImageSerializer,
            "pdf": DocumentSerializer,
            "rich_text": RichTextSerializer,
        }
    )

    @staticmethod
    def get_image_url(obj: Article):
        if obj.image:
            return obj.image.file.url
        return None

    class Meta:
        abstract = True


class BlogPostSerializer(ArticleSerializer):
    class Meta:
        model = BlogPost
        fields = ARTICLE_FIELDS


class ResourceSerializer(ArticleSerializer):
    class Meta:
        model = Resource
        fields = ARTICLE_FIELDS


class PartnerSerializer(serializers.ModelSerializer):
    logo_image_url = serializers.SerializerMethodField()

    @staticmethod
    def get_logo_image_url(obj: Partner):
        if obj.logo_image:
            return obj.logo_image.file.url
        return None

    class Meta:
        model = Partner
        fields = ["id", "name", "logo_image_url", "height", "show_in_home_page"]


class PersonSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    @staticmethod
    def get_image_url(obj: Person):
        if obj.image:
            return obj.image.file.url
        return None

    class Meta:
        model = Person
        fields = ["id", "name", "image_url", "job_title"]
