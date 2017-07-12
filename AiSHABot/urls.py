from django.conf.urls import url
from AiSHABot.views import AiSHAView

urlpatterns = [
    url(r'^7a8bc5f20d6c86b3021a74a4a1bca1bbe411ea6b9f04628f6a/?$', AiSHAView.as_view())
]