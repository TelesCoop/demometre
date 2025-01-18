from rest_framework import serializers
from open_democracy_back.models.settings_models import (
    ImportantPagesSettings,
    RGPDSettings,
    StructureSettings,
)
from open_democracy_back.serializers.page_serializers import ContentPageSerializer


class StructureSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StructureSettings
        fields = ["email"]
        read_only_fields = fields


class RGPDSettingsSerializer(serializers.ModelSerializer):
    legal_mention_url = serializers.SerializerMethodField()
    terms_of_use_url = serializers.SerializerMethodField()
    terms_of_sale_url = serializers.SerializerMethodField()
    confidentiality_policy_url = serializers.SerializerMethodField()
    content_license_url = serializers.SerializerMethodField()

    @staticmethod
    def get_legal_mention_url(obj: RGPDSettings):
        if obj.legal_mention:
            return obj.legal_mention.file.url
        return None

    @staticmethod
    def get_terms_of_use_url(obj: RGPDSettings):
        if obj.terms_of_use:
            return obj.terms_of_use.file.url
        return None

    @staticmethod
    def get_terms_of_sale_url(obj: RGPDSettings):
        if obj.terms_of_sale:
            return obj.terms_of_sale.file.url
        return None

    @staticmethod
    def get_confidentiality_policy_url(obj: RGPDSettings):
        if obj.confidentiality_policy:
            return obj.confidentiality_policy.file.url
        return None

    @staticmethod
    def get_content_license_url(obj: RGPDSettings):
        if obj.content_license:
            return obj.content_license.file.url
        return None

    class Meta:
        model = RGPDSettings
        fields = [
            "legal_mention_url",
            "terms_of_use_url",
            "terms_of_sale_url",
            "confidentiality_policy_url",
            "content_license_url",
        ]
        read_only_fields = fields


class ImportantPagesSettingsSerializer(serializers.ModelSerializer):
    faq_page = serializers.SerializerMethodField()

    @staticmethod
    def get_faq_page(obj: ImportantPagesSettings):
        page = obj.faq_page.specific
        return ContentPageSerializer(page).data

    class Meta:
        model = ImportantPagesSettings
        fields = [
            "faq_page",
        ]
        read_only_fields = fields
