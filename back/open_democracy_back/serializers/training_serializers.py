from rest_framework import serializers

from open_democracy_back.models import Training


class TrainingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Training
        fields = (
            "audience",
            "description",
            "duration",
            "id",
            "is_available_soon",
            "name",
            "url",
        )

    url = serializers.SerializerMethodField()

    def get_url(self, obj: Training):
        if obj.link:
            return obj.link
        if obj.file:
            return obj.file.url
