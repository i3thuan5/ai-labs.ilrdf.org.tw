from django.shortcuts import render

# Create your views here.
from bangtsam.models import HomePage, SitemapPage, \
    IntroPage, FeedbackPage, ApplicationFormPage, \
    AboutUsPage, TermsOfUsePage, CopyrightPage
from django.views.decorators.http import require_GET


@require_GET
def comming_soon_view(request):
    return render(request, 'bangtsam/comming_soon.html')
