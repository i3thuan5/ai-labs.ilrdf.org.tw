from pathlib import Path

from django.core.exceptions import ValidationError
from wagtail.blocks import CharBlock, RichTextBlock
from wagtail.blocks import StructBlock, StructBlockValidationError
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.embeds.blocks import EmbedBlock


class SampleBlock(StructBlock):
    tribe = CharBlock()
    sample_text = CharBlock()
    translation_text = CharBlock()
    audio = DocumentChooserBlock()

    def clean(self, value):
        result = super().clean(value)
        audio = result["audio"]
        file_type = ''.join(Path(audio.file.path).suffixes)
        if file_type != '.wav':
            raise StructBlockValidationError(block_errors={
                "audio": ValidationError("音檔欄位限定上傳.wav格式")
            })
        return result

    class Meta:
        icon = 'media'
        min_num = 0


class YoutubeBlock(StructBlock):
    class Meta:
        template = "blocks/youtube.html"

    title = CharBlock()
    youtube_url = EmbedBlock(max_width=560)
    accessibility_text = RichTextBlock()
