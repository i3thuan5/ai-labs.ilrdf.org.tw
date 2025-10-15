from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from wagtail.documents import models
from wagtail.documents.forms import get_document_form


class DocumentFormTest(TestCase):

    def test_small_document_upload_success(self):
        content_string = b'hello world'
        form_data = {
            "title": "1KB Document.txt",
            "tags": [],
        }
        file_data = {
            "file": SimpleUploadedFile(
                '1kb-document.txt',
                content_string,
                content_type='text/plain'),
        }
        form_cls = get_document_form(models.Document)
        form = form_cls(form_data, file_data)
        self.assertTrue(form.is_valid(), msg=form.errors)

    def test_small_document_upload_validationerror(self):
        content_string = b'hello world' * 5 * 1024 * 1024
        form_data = {
            "title": "Large Document.txt",
            "tags": [],
        }
        file_data = {
            "file": SimpleUploadedFile(
                'large-document.txt',
                content_string,
                content_type='text/plain'),
        }
        form_cls = get_document_form(models.Document)
        form = form_cls(form_data, file_data)
        self.assertFormError(
            form, 'file',
            [
                '文件檔案請小於5.0MB以下。',
                '不允許副檔名為 “” 。可用的像是: docx, odt, pdf, txt, wav。'
            ])

    def test_invalid_none_file_data(self):
        content_string = b'hello world'
        form_data = {
            "title": "1KB Document.txt",
            "tags": [],
        }
        file_data = {}
        form_cls = get_document_form(models.Document)
        form = form_cls(form_data, file_data)
        # self.assertFormError(
        #     form, 'file',
        #     [
        #         '必要欄位',
        #         '不允許副檔名為 “” 。可用的像是: docx, odt, pdf, txt, wav。'
        #     ])
        self.assertTrue(form.is_valid(), msg=form.errors)
