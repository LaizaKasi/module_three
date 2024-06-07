from django.urls import path
from .views import translate_view, paraphrase_view, summarize_view

urlpatterns = [
    path('translate/', translate_view, name='translate'),
    path('paraphrase/', paraphrase_view, name='paraphrase'),
    path('summarize/', summarize_view, name='summarize'),
]
