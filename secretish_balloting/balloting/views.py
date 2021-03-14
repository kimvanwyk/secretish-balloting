from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Ballot, Question, Choice, Voter


def vote(request, ballot_fragment, voter_fragment):
    ballot = get_object_or_404(Ballot, url_fragment_text=ballot_fragment)
    voter = get_object_or_404(Voter, url_fragment_text=voter_fragment)
    questions = Question.objects.filter(ballot=ballot).order_by("order_int").all()
    questions = Question.objects.filter(ballot=ballot).order_by("order_int").all()
    if request.method == "POST":
        choices = {
            q.order_int: request.POST.get(f"question{q.order_int}_choice")
            for q in questions
            if request.POST.get(f"question{q.order_int}_choice")
        }
        if len(choices) == len(questions):
            return HttpResponse(f"Thanks for voting")
        else:
            error_message = "Please select an option for each question"
    else:
        error_message = None
    return render(
        request,
        "balloting/vote.html",
        {
            "ballot": ballot,
            "voter": voter,
            "questions": questions,
            "error_message": error_message,
        },
    )
