from django.urls import path, include
from rest_framework import routers

from .views import AddCandidateView, GetAllCandidates, VoteCandidate

app_name = 'add_and_vote'

urlpatterns = [
    path('add/', AddCandidateView.as_view()),
    path('all-candidates/', GetAllCandidates.as_view()),
    path('vote/<int:pk>/', VoteCandidate.as_view()),
]