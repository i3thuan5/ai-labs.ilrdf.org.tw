
from bangtsam.models import HomePage, SitemapPage, \
    IntroPage, FeedbackPage, ApplicationFormPage, \
    AboutUsPage, TermsOfUsePage, CopyrightPage
from django.conf import settings


def theh_wagtail_pages(request):
    context = {}
    context['homepage'] = HomePage.objects.live().first()
    context['sitemappage'] = SitemapPage.objects.live().first()
    context['intropage'] = IntroPage.objects.live().first()
    context['feedbackpage'] = FeedbackPage.objects.live().first()
    context['applicationformpage'] = ApplicationFormPage.objects.live().first()
    context['aboutuspage'] = AboutUsPage.objects.live().first()
    context['termofusepage'] = TermsOfUsePage.objects.live().first()
    context['copyrightpage'] = CopyrightPage.objects.live().first()
    return context


def theh_ai_url(request):
    context = {}
    return {
        "ai_url": {
            "asr": settings.SAPOLITA_ASR_URL,
            "tts": settings.SAPOLITA_TTS_URL,
            "translate": settings.SAPOLITA_TRANSLATE_URL,
        }
    }
