from collections import defaultdict, Counter
import os

from django.contrib.admin.views.decorators import staff_member_required
from django.core.mail import send_mass_mail
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from dotenv import load_dotenv

from .models import Ballot, Question, Choice, Voter, Vote

load_dotenv()


def vote(request, ballot_fragment, voter_fragment):
    ballot = get_object_or_404(Ballot, url_fragment_text=ballot_fragment)
    dt = timezone.now()
    if dt < ballot.opening_date:
        return HttpResponse(
            f"<h2>The {ballot.name_text} ballot has not opened yet. It will open at {ballot.opening_date:%H:%M SAST on %d %B %Y}</h2>"
        )
    if dt > ballot.closing_date:
        return HttpResponse(
            f"<h2>The {ballot.name_text} ballot closed at {ballot.closing_date:%H:%M SAST on %d %B %Y}.</h2>"
        )
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
    dt = timezone.now()
    if dt < ballot.opening_date:
        return HttpResponse(
            f"<h2>The {ballot.name_text} ballot has not opened yet. It will open at {ballot.opening_date:%H:%M SAST on %d %B %Y}</h2>"
        )
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
            "closed": dt > ballot.closing_date,
        },
    )


def ballot_results(request, ballot_fragment):
    ballot = get_object_or_404(
        Ballot,
        url_fragment_text=ballot_fragment,
    )
    num_voters = len(Voter.objects.filter(ballot=ballot).all())
    votes = (
        Vote.objects.filter(choice__question__ballot=ballot)
        .order_by("choice__question__order_int")
        .all()
    )
    results_dict = defaultdict(Counter)
    questions = Question.objects.filter(ballot=ballot).all()
    for question in questions:
        for choice in Choice.objects.filter(question=question).all():
            results_dict[question][choice] = 0
    for v in votes:
        results_dict[v.choice.question][v.choice] += 1
    results_list = []
    for (question, choices) in results_dict.items():
        cl = [
            [frequency, choice.choice_text] for (choice, frequency) in choices.items()
        ]
        cl.sort(reverse=True)
        num_votes = len([c for c in cl if c[0]])
        for c in cl:
            if num_votes == 0:
                percentage = 0
            else:
                percentage = c[0] / (num_votes * 1.0) * 100.0
            c.append(f"{percentage:.2f}")
        if num_voters == 0:
            percentage = 0
        else:
            percentage = num_votes / (num_voters * 1.0) * 100.0
        results_list.append(
            (
                question.order_int,
                question.question_text,
                num_votes,
                num_voters,
                f"{percentage:.2f}",
                cl,
            )
        )
    results_list.sort()
    return render(
        request,
        "balloting/results.html",
        {
            "ballot": ballot,
            "now": timezone.now(),
            "results": results_list,
        },
    )


@staff_member_required
def email_unemailed(request):
    voters = Voter.objects.filter(emailed_bool=False)
    if request.method == "GET":
        return render(request, "balloting/emailer.html", {"voters": voters})
    with open("balloting/email_templates/instructions.txt") as fh:
        template = fh.read()
    emails = []
    for voter in voters:
        ballot = Ballot.objects.filter(voter=voter).first()
        url = reverse(
            "balloting:vote",
            args=(
                ballot.url_fragment_text,
                voter.url_fragment_text,
            ),
        )
        msg = template.format(
            **{
                "ballot_name": ballot.name_text,
                "contact_name": os.getenv("CONTACT_NAME"),
                "contact_email": os.getenv("CONTACT_EMAIL"),
                "url": f"{os.getenv('BASE_URL')}{url}",
            }
        )

        emails.append(
            (
                f"Voting details for the {ballot.name_text} ballot",
                msg,
                os.getenv("FROM_EMAIL"),
                [voter.email_text],
            )
        )
    if emails:
        try:
            send_mass_mail(emails)
        except Exception as e:
            return HttpResponse(f"Error sending emails: {e}")
        for voter in voters:
            voter.emailed_bool = True
            voter.save()
            return HttpResponse(
                f"<h2>{len(emails)} email{'s' if len(emails) > 1 else ''} sent.</h2>"
            )
    return HttpResponse(
        f"<h2>All voters have been emailed before - no emails were sent.</h2>"
    )
