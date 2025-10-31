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
        context={
            'page': {
                'title': '500 - 網站內部錯誤',
                'search_description': '網站內部錯誤',
                'body': (''
                         ),
            },
        },
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
                'body': (
                    '''<p>頁面可能被刪除、移動，或是網址輸入錯誤。'''
                    '''您可點擊目前瀏覽器返回上一頁的功能，'''
                    '''或利用主選單回到首頁。</p>'''
                ),
            },
        },
        status=404
    )
