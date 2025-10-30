from django.shortcuts import render
from django.views.decorators.http import require_GET


@require_GET
def comming_soon_view(request):
    return render(request, 'bangtsam/comming_soon.html')


@require_GET
def webmanifest_view(request):
    return render(request, 'khing/site.webmanifest')


@require_GET
def handle500(request):
    return render(
        request,
        'handler/handler.html',
        context={},
        status=500
    )


@require_GET
def handle404(request, exception):
    return render(
        request,
        'handler/handler.html',
        context={
            'page': {
                'title': '404錯誤 - 找不到此頁面',
                'search_description': '找不到此頁面',
                'body': (''
                         ),
            },
        },
        status=404
    )
