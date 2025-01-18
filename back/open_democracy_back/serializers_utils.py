from rest_framework import serializers

from django.utils import translation
from open_democracy_back.settings.base import DEFAULT_LOCALE


def method_for_translated_field(field_name):
    @staticmethod
    def my_function(obj):
        locale = translation.get_language()
        if field_name == "explanatory":
            return list(getattr(obj, f"{field_name}_{locale}").raw_data or []) or list(
                getattr(obj, f"{field_name}_{DEFAULT_LOCALE}").raw_data or []
            )
        else:
            return getattr(obj, f"{field_name}_{locale}") or getattr(
                obj, f"{field_name}_{DEFAULT_LOCALE}"
            )

    my_function.__name__ = f"get_{field_name}"
    return my_function


class SerializerWithTranslatedFields(serializers.ModelSerializer):
    """
    Serializer that looks for translated fields in the original model,
    and creates a SerializerMethodField for each of them.

    The method will return the content in the current locale.
    """

    def __new__(cls, *args, **kwargs):
        for field in getattr(cls.Meta.model, "translated_fields", []):
            setattr(cls, field, serializers.SerializerMethodField())
            setattr(cls, f"get_{field}", method_for_translated_field(field))
            # if not explicitly declared here, the Method will be ignored
            getattr(cls, "_declared_fields")[
                field
            ] = serializers.SerializerMethodField()
        return super().__new__(cls, *args, **kwargs)


SOURCE_SEPARATOR = "."


def get_lookup_relation(obj, source):
    relation = source.split(SOURCE_SEPARATOR)
    if len(relation) == 1:
        return (obj, source)
    new_obj = getattr(obj, relation[0])
    new_source = SOURCE_SEPARATOR.join(relation[1:])
    return get_lookup_relation(new_obj, new_source)


class TranslatedField(serializers.CharField):
    """
    Serializer field that returns the content in the current locale.
    """

    def __init__(self, source=None, **kwargs):
        self.custom_source = source
        kwargs["source"] = "*"
        kwargs["read_only"] = True
        super().__init__(**kwargs)

    def to_representation(self, obj):
        locale = translation.get_language()

        source = self.custom_source
        if source:
            obj_of_interest, source = get_lookup_relation(obj, source)
        else:
            source = self.field_name
            obj_of_interest = obj

        return getattr(obj_of_interest, f"{source}_{locale}") or getattr(
            obj_of_interest, f"{source}_{DEFAULT_LOCALE}"
        )
