# most of the content comes from https://gist.github.com/thclark/100d6aa6d0995984589b983f896002d4
from rest_framework.fields import Field
from wagtail.blocks import StreamBlock, ListBlock, StructBlock
from rest_framework import serializers


class SerializerStreamField(Field):
    """
    see https://gist.github.com/thclark/100d6aa6d0995984589b983f896002d4
    Serializes StreamField values.
    Stream fields are stored in JSON format in the database. We reuse that in
    the API.
    Example:
    "body": [
        {
            "type": "heading",
            "value": {
                "text": "Hello world!",
                "size": "h1"
            }
        },
        {
            "type": "paragraph",
            "value": "Some content"
        }
        {
            "type": "image",
            "value": 1
        }
    ]
    Where "heading" is a struct block containing "text" and "size" fields, and "paragraph" is a simple text block.
    NOTE: foreign keys are represented slightly differently in stream fields compared to other parts of the wagtail API.
    In stream fields, a foreign key is represented by an integer (the ID of the related object) but elsewhere in the API,
    foreign objects are nested objects with id and meta as attributes.
    This creates problems, in particular, for serialising images - since for each image, you need a second call to the
    API to find its URL then create the page. Yet another example of Wagtail's weird customisations being very
    unhelpful.
    You can override the behaviour using get_api_representation **at the model or snippet level**
    So, I drilled into the StreamField code, and pulled out where the actual serialization happens. Here, we treat the
    api representation built into the block as default; but can override it for specific block names.
    """

    def __init__(self, *args, **kwargs):
        self.serializers = kwargs.pop("serializers", object())
        self.recurse = False  # kwargs.pop('recurse', True) --- Recursion not working yet; see below
        super().__init__(*args, **kwargs)

    def to_representation(self, value, ctr=0):
        # print('AT RECURSION LEVEL:', ctr)
        representation = []
        if value is None:
            return representation

        for stream_item in value:
            # print('Stream item type:', type(stream_item))

            # If there's a serializer for the child block type in the mapping, switch to it
            if stream_item.block.name in self.serializers.keys():
                item_serializer = self.serializers[stream_item.block.name]
                if item_serializer is not None:
                    # print('Switching to specified serializer {} for stream_item {}'.format(
                    #     self.serializers[stream_item.block.name].__class__.__name__,
                    #     stream_item.block.name
                    # ))
                    item_representation = item_serializer(
                        context=self.context
                    ).to_representation(stream_item.value)
                else:
                    print(
                        "Specified serializer for child {} is explicitly set to None - using default API representation for block:",
                        stream_item.block.name,
                    )
                    item_representation = stream_item.block.get_api_representation(
                        stream_item.value, context=self.context
                    )

            # If recursion is turned on, recurse through structural blocks using the present serializer mapping
            # TODO the blocks data structure is borked. Nodes and leaves are flattened together so I can't recurse down the tree straightforwardly.
            #  I have to apply the default representation at this level since it works on the whole block, then extract child items that are either custom-mapped or
            #  structural and recurse down only those, zipping their results back together. Spent several hours, leaving it until someone has a very strong use case.
            elif self.recurse and isinstance(
                stream_item.block,
                (
                    StructBlock,
                    StreamBlock,
                    ListBlock,
                ),
            ):
                # print('Recursing serialiser for structural block::', stream_item.block.name)
                item_representation = self.to_representation(stream_item.value)

            else:
                # print('No recursion, or leaf node reached with no specified serializer mapping for block:', stream_item.block.name)
                item_representation = stream_item.block.get_api_representation(
                    stream_item.value, context=self.context
                )

            representation.append(
                {
                    "type": stream_item.block.name,
                    "value": item_representation,
                    "id": stream_item.id,
                }
            )

        return representation


class DocumentSerializer(serializers.Serializer):
    url = serializers.FileField(source="document")
    title = serializers.CharField()

    class Meta:
        fields = ("url", "title")


class ImageSerializer(serializers.Serializer):
    url = serializers.SerializerMethodField()
    caption = serializers.CharField()

    class Meta:
        fields = ("url", "caption")

    def get_url(self, obj):
        return obj["image"].file.url


class RichTextSerializer(serializers.Serializer):
    html = serializers.SerializerMethodField()

    class Meta:
        fields = ("html",)

    def get_html(self, obj):
        return obj.source
