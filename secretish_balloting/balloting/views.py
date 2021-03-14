from collections import defaultdict, Counter

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Ballot, Question, Choice, Voter, Vote


def vote(request, ballot_fragment, voter_fragment):
    ballot = get_object_or_404(Ballot, url_fragment_text=ballot_fragment)
    voter = get_object_or_404(Voter, url_fragment_text=voter_fragment)
    questions = Question.objects.filter(ballot=ballot).order_by("order_int").all()
    if request.method == "POST":
        choices = [
            int(request.POST.get(f"question{q.order_int}_choice"))
            for q in questions
            if request.POST.get(f"question{q.order_int}_choice")
        ]
        if len(choices) == len(questions):
            votes = Vote.objects.filter(voter=voter).all()
            if votes:
                votes.delete()
            for choice in choices:
                v = Vote(voter=voter, choice_id=choice)
                v.save()
            return HttpResponseRedirect(
                reverse(
                    "balloting:voting_summary",
                    args=(
                        ballot_fragment,
                        voter_fragment,
                    ),
                )
            )
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


def voting_summary(request, ballot_fragment, voter_fragment):
    ballot = get_object_or_404(Ballot, url_fragment_text=ballot_fragment)
    voter = get_object_or_404(Voter, url_fragment_text=voter_fragment)
    votes = (
        Vote.objects.filter(voter=voter).order_by("choice__question__order_int").all()
    )
    summary = [(v.choice.question.question_text, v.choice.choice_text) for v in votes]
    return render(
        request,
        "balloting/summary.html",
        {
            "ballot": ballot,
            "voter": voter,
            "summary": summary,
        },
    )
