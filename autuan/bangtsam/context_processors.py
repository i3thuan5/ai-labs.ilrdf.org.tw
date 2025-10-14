
from bangtsam.models import HomePage, SitemapPage, \
    IntroPage, FeedbackPage, ApplicationFormPage, \
    AboutUsPage, TermsOfUsePage, CopyrightPage


def theh_wagtail_pages(request):
    context = {}
    context['homepage'] = HomePage.objects.first()
    context['sitemappage'] = SitemapPage.objects.first()
    context['intropage'] = IntroPage.objects.first()
    context['feedbackpage'] = FeedbackPage.objects.first()
    context['applicationformpage'] = ApplicationFormPage.objects.first()
    context['aboutuspage'] = AboutUsPage.objects.first()
    context['termofusepage'] = TermsOfUsePage.objects.first()
    context['copyrightpage'] = CopyrightPage.objects.first()
    return context
