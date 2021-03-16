from django.urls import path

from . import views

app_name = "balloting"
urlpatterns = [
    path("emailer/", views.email_unemailed, name="email_unemailed"),
    path(
        "<str:ballot_fragment>/<str:summary_fragment>/results/",
        views.ballot_results,
        name="ballot_results",
    ),
    path("<str:ballot_fragment>/<str:voter_fragment>/", views.vote, name="vote"),
    path(
        "<str:ballot_fragment>/<str:voter_fragment>/summary/",
        views.voting_summary,
        name="voting_summary",
    ),
]
