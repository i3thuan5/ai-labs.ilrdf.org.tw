from django.conf import settings
from wagtail.documents.forms import BaseDocumentForm


class CustomDocumentForm(BaseDocumentForm):

    def clean(self):
        cleaned_data = super().clean()
        file_max_size = settings.CUSTOM_WAGTAILDOCS_MAX_UPLOAD_SIZE
        if (
            "file" in cleaned_data
            and cleaned_data["file"].size > file_max_size
        ):
            max_size_mb = file_max_size / (1024*1024)
            self.add_error("file", f"文件檔案請小於{max_size_mb}MB以下。")
        return cleaned_data
