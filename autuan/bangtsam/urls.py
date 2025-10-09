from django.urls import path

from bangtsam.views import comming_soon_view

urlpatterns = [
    path('comming_soon/', comming_soon_view, name='comming_soon'),
]
