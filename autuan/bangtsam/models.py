import re

from django.db import models
from django.core.exceptions import ValidationError
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.forms import WagtailAdminPageForm
from wagtail.admin.panels import FieldPanel

from bangtsam.blocks import SampleBlock


class KongkeIahForm(WagtailAdminPageForm):

    def clean_slug(self):
        slug = self.cleaned_data['slug']
        if re.search(r"[^a-z0-9-]", slug):
            raise ValidationError('限定小寫字母a到z、數字0到9、半型連接號-。')
        return slug


class HomePage(Page):
    parent_page_types = ['wagtailcore.Page']
    max_count_per_parent = 1

    template = 'bangtsam/homepage.html'
    base_form_class = KongkeIahForm

    def get_context(self, request):
        context = super().get_context(request)
        homepage = HomePage.objects.first()
        intropage = IntroPage.objects.first()
        feedbackpage = FeedbackPage.objects.first()
        applicationformpage = ApplicationFormPage.objects.first()
        aboutuspage = AboutUsPage.objects.first()
        termofusepage = TermsOfUsePage.objects.first()
        copyrightpage = CopyrightPage.objects.first()
        sitemappage = SitemapPage.objects.first()
        context['homepage'] = homepage
        context['sitemappage'] = sitemappage
        context['intropage'] = intropage
        context['feedbackpage'] = feedbackpage
        context['applicationformpage'] = applicationformpage
        context['aboutuspage'] = aboutuspage
        context['termofusepage'] = termofusepage
        context['copyrightpage'] = copyrightpage
        return context


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

    def get_context(self, request):
        context = super().get_context(request)
        homepage = HomePage.objects.first()
        sitemappage = SitemapPage.objects.first()
        intropage = IntroPage.objects.first()
        feedbackpage = FeedbackPage.objects.first()
        applicationformpage = ApplicationFormPage.objects.first()
        aboutuspage = AboutUsPage.objects.first()
        termofusepage = TermsOfUsePage.objects.first()
        copyrightpage = CopyrightPage.objects.first()
        context['homepage'] = homepage
        context['sitemappage'] = sitemappage
        context['intropage'] = intropage
        context['feedbackpage'] = feedbackpage
        context['applicationformpage'] = applicationformpage
        context['aboutuspage'] = aboutuspage
        context['termofusepage'] = termofusepage
        context['copyrightpage'] = copyrightpage
        return context


class SitemapPage(RichTextBasePage):
    template = 'bangtsam/richtextbase.html'


class IntroPage(RichTextBasePage):
    template = 'bangtsam/richtextbase.html'


class FeedbackPage(RichTextBasePage):
    feedbackurl = models.URLField(blank=True, help_text="意見回饋的Google表單連結")

    template = 'bangtsam/feedbackpage.html'
    content_panels = Page.content_panels + [
        FieldPanel('body'),
        FieldPanel('feedbackurl'),
    ]


class ApplicationFormPage(RichTextBasePage):
    sample = StreamField([
        ('sample_block', SampleBlock()),
    ],
        blank=True,
        null=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel('body'),
        FieldPanel('sample'),
    ]

    template = 'bangtsam/applicationformpage.html'


class AboutUsPage(RichTextBasePage):
    template = 'bangtsam/richtextbase.html'


class CopyrightPage(RichTextBasePage):
    template = 'bangtsam/richtextbase.html'


class TermsOfUsePage(RichTextBasePage):
    template = 'bangtsam/richtextbase.html'
