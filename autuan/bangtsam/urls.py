from django.urls import path

from bangtsam.views import comming_soon_view, webmanifest_view, ga_pv_view

urlpatterns = [
    path('comming_soon/', comming_soon_view, name='comming_soon'),
    path('webmanifest/', webmanifest_view, name='webmanifest'),
    path('ga-pv/', ga_pv_view, name='ga_pv'),
]
