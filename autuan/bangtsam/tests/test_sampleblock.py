from django.test import TestCase
from django.core.exceptions import ValidationError
from wagtail.documents import get_document_model

from bangtsam.blocks import SampleBlock
from bangtsam.tests.utils import get_test_document_file


class SampleBlockTest(TestCase):
    def test_clean_bad_audio_raise_validationerror(self):
        block = SampleBlock()
        fake_file = get_document_model().objects.create(
            title="Mini document",
            file=get_test_document_file(file_suffix='txt'),
        )
        bad_data = {
            'tribe': 'Pangcah',
            'sample_text': 'Maranam',
            'translation_text': '早安。',
            'audio': fake_file,
        }
        with self.assertRaises(ValidationError):
            block.clean(bad_data)

    def test_clean_valid_audio(self):
        block = SampleBlock()
        fake_file = get_document_model().objects.create(
            title="Mini wav",
            file=get_test_document_file(file_suffix='wav'),
        )
        good_data = {
            'tribe': 'Pangcah',
            'sample_text': 'Maranam',
            'translation_text': '早安。',
            'audio': fake_file,
        }
        cleaned_data = block.clean(good_data)
        self.assertEqual(cleaned_data['audio'].title, "Mini wav")
