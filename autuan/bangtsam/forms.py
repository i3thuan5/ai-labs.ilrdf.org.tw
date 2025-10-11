import re

from django.core.exceptions import ValidationError
from wagtail.admin.forms import WagtailAdminPageForm


class KongkeIahForm(WagtailAdminPageForm):

    def clean_slug(self):
        slug = self.cleaned_data['slug']
        if re.search(r"[^a-z0-9-]", slug):
            raise ValidationError('限定小寫字母a到z、數字0到9、半型連接號-。')
        return slug
