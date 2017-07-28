from django.conf.urls import url
from TrafficGuru import views

urlpatterns = [
    url(r'^7a8bc5f20d6c86b3021a74a4a1bca1bbe411ea6b9f04628f6a/?$', views.TrafficGuruView.as_view()),
    url(r'^privacy', views.privacy)
]