from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel


class HomePage(Page):
    parent_page_types = ['wagtailcore.Page']
    max_count_per_parent = 1

    template = 'bangtsam/homepage.html'


class RichTextBasePage(Page):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]

    parent_page_types = ['HomePage']
    subpage_types = []
    max_count_per_parent = 1

    class Meta:
        abstract = True


class SitemapPage(RichTextBasePage):
    pass


class IntroPage(RichTextBasePage):
    pass


class FeedbackPage(RichTextBasePage):
    pass


class ApplicationFormPage(RichTextBasePage):
    pass


class AboutUsPage(RichTextBasePage):
    pass


class TermsOfUsePage(RichTextBasePage):
    pass
