from django.conf.urls import url
from .views import RailMitraView, privacypolicy
urlpatterns = [
    url(r'^thisissecret75aef2b9-073e-458d-9cd6-e3e7795ea9c2/?$', RailMitraView.as_view()),
    url(r'^privacypolicy/', privacypolicy)
]