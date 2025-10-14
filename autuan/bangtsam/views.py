from django.shortcuts import render
from django.views.decorators.http import require_GET


@require_GET
def comming_soon_view(request):
    return render(request, 'bangtsam/comming_soon.html')
