from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel


class HomePage(Page):
    parent_page_types = ['wagtailcore.Page']
    max_count_per_parent = 1

    template = 'bangtsam/homepage.html'

    def get_context(self, request):
        context = super().get_context(request)
        sitemappage = SitemapPage.objects.first()
        intropage = IntroPage.objects.first()
        feedbackpage = FeedbackPage.objects.first()
        applicationformpage = ApplicationFormPage.objects.first()
        aboutuspage = AboutUsPage.objects.first()
        termofusepage = TermsOfUsePage.objects.first()
        context['sitemappage'] = sitemappage
        context['intropage'] = intropage
        context['feedbackpage'] = feedbackpage
        context['applicationformpage'] = applicationformpage
        context['aboutuspage'] = aboutuspage
        context['termofusepage'] = termofusepage
        return context


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

    def get_context(self, request):
        context = super().get_context(request)
        sitemappage = SitemapPage.objects.first()
        intropage = IntroPage.objects.first()
        feedbackpage = FeedbackPage.objects.first()
        applicationformpage = ApplicationFormPage.objects.first()
        aboutuspage = AboutUsPage.objects.first()
        termofusepage = TermsOfUsePage.objects.first()
        context['sitemappage'] = sitemappage
        context['intropage'] = intropage
        context['feedbackpage'] = feedbackpage
        context['applicationformpage'] = applicationformpage
        context['aboutuspage'] = aboutuspage
        context['termofusepage'] = termofusepage
        return context


class SitemapPage(RichTextBasePage):
    template = 'bangtsam/richtextbase.html'


class IntroPage(RichTextBasePage):
    template = 'bangtsam/richtextbase.html'


class FeedbackPage(RichTextBasePage):
    template = 'bangtsam/richtextbase.html'


class ApplicationFormPage(RichTextBasePage):
    template = 'bangtsam/richtextbase.html'


class AboutUsPage(RichTextBasePage):
    template = 'bangtsam/richtextbase.html'


class TermsOfUsePage(RichTextBasePage):
    template = 'bangtsam/richtextbase.html'
