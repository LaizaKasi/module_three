from django.urls import path
from .views import translate_view, paraphrase_view, summarise_view

urlpatterns = [
    path('translate/', translate_view, name='translate'),
    path('paraphrase/', paraphrase_view, name='paraphrase'),
    path('summarise/', summarise_view, name='summarize'),
]
