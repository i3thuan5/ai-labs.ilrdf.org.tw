from django.shortcuts import render

# Create your views here.
from bangtsam.models import HomePage, SitemapPage, \
    IntroPage, FeedbackPage, ApplicationFormPage,\
    AboutUsPage, TermsOfUsePage, CopyrightPage


def comming_soon_view(request):
    homepage = HomePage.objects.first()
    sitemappage = SitemapPage.objects.first()
    intropage = IntroPage.objects.first()
    feedbackpage = FeedbackPage.objects.first()
    applicationformpage = ApplicationFormPage.objects.first()
    aboutuspage = AboutUsPage.objects.first()
    termofusepage = TermsOfUsePage.objects.first()
    copyrightpage = CopyrightPage.objects.first()
    context = dict()
    context['homepage'] = homepage
    context['sitemappage'] = sitemappage
    context['intropage'] = intropage
    context['feedbackpage'] = feedbackpage
    context['applicationformpage'] = applicationformpage
    context['aboutuspage'] = aboutuspage
    context['termofusepage'] = termofusepage
    context['copyrightpage'] = copyrightpage
    return render(request, 'bangtsam/comming_soon.html', context)
