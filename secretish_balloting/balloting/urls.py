from django.urls import path

from . import views

app_name = "balloting"
urlpatterns = [
    path("<str:ballot_fragment>/<str:voter_fragment>/", views.vote, name="vote"),
    path(
        "<str:ballot_fragment>/<str:voter_fragment>/submit",
        views.submit_vote,
        name="submit_vote",
    ),
]
