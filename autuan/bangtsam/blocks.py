from wagtail import blocks
from wagtail.images.blocks import ImageBlock
from wagtail.documents.blocks import DocumentChooserBlock

# class PersonBlock(blocks.StructBlock):
#     mia = blocks.CharBlock()
#     photo = ImageBlock(required=False)
#     biography = blocks.RichTextBlock()

#     class Meta:
#         icon = 'user'
#         form_attrs = {
#             # This block has additional customizations enabled
#             'data-controller': 'magic',
#             'data-action': 'click->magic#abracadabra',
#         }


class SampleBlock(blocks.StructBlock):
    tribe = blocks.CharBlock()
    sample_text = blocks.CharBlock()
    translation_text = blocks.CharBlock()
    audio = DocumentChooserBlock()

    class Meta:
        icon = 'media'
