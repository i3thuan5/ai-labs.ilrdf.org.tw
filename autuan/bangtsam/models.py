from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel

from bangtsam.blocks import SampleBlock
from bangtsam.forms.admin_page import KongkeIahForm


BANGTSAM_RICHTEXTBASE_HTML = 'bangtsam/richtextbase.html'


class HomePage(Page):
    parent_page_types = ['wagtailcore.Page']
    max_count_per_parent = 1

    template = 'bangtsam/homepage.html'
    base_form_class = KongkeIahForm


class RichTextBasePage(Page):
    body = RichTextField(
        blank=True,
        features=['h2', 'h3', 'bold', 'italic',
                  'link', 'ol', 'ul', 'document-link',
                  'image', ])

    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]

    parent_page_types = ['HomePage']
    subpage_types = []
    max_count_per_parent = 1
    base_form_class = KongkeIahForm

    class Meta:
        abstract = True


class SitemapPage(RichTextBasePage):
    template = BANGTSAM_RICHTEXTBASE_HTML


class IntroPage(RichTextBasePage):
    template = BANGTSAM_RICHTEXTBASE_HTML


class FeedbackPage(RichTextBasePage):
    feedbackurl = models.URLField(blank=True, help_text="意見回饋的Google表單連結")

    template = 'bangtsam/feedbackpage.html'
    content_panels = Page.content_panels + [
        FieldPanel('body'),
        FieldPanel('feedbackurl'),
    ]


class ApplicationFormPage(RichTextBasePage):
    sample_title = models.CharField(max_length=255, blank=True, null=True)
    sample = StreamField([
        ('sample_block', SampleBlock()),
    ],
        blank=True,
        null=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel('body'),
        FieldPanel('sample_title'),
        FieldPanel('sample'),
    ]

    template = 'bangtsam/applicationformpage.html'


class AboutUsPage(RichTextBasePage):
    template = BANGTSAM_RICHTEXTBASE_HTML


class CopyrightPage(RichTextBasePage):
    template = BANGTSAM_RICHTEXTBASE_HTML


class TermsOfUsePage(RichTextBasePage):
    template = BANGTSAM_RICHTEXTBASE_HTML
