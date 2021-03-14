from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Ballot, Question, Choice, Voter


def vote(request, ballot_fragment, voter_fragment):

    ballot = get_object_or_404(Ballot, url_fragment_text=ballot_fragment)
    voter = get_object_or_404(Voter, url_fragment_text=voter_fragment)
    questions = Question.objects.filter(ballot=ballot).order_by("order_int").all()

    return render(
        request,
        "balloting/vote.html",
        {"ballot": ballot, "voter": voter, "questions": questions},
    )


def submit_vote(request, ballot_fragment, voter_fragment):
    ballot = get_object_or_404(Ballot, url_fragment_text=ballot_fragment)
    voter = get_object_or_404(Voter, url_fragment_text=voter_fragment)
    questions = Question.objects.filter(ballot=ballot).order_by("order_int").all()
    print([f"question{q.order_int}_choice" for q in questions])
    print(request.POST)
    choices = {
        q.order_int: request.POST.get(f"question{q.order_int}_choice")
        for q in questions
        if request.POST.get(f"question{q.order_int}_choice")
    }
    print(choices, len(choices), len(questions))
    if len(choices) != len(questions):
        return render(
            request,
            "balloting/vote.html",
            {
                "ballot": ballot,
                "voter": voter,
                "questions": questions,
                "error_message": "Please select an option for each question",
            },
        )
    return HttpResponse(f"Thanks for voting")

    # question = get_object_or_404(Question, pk=question_id)
    # try:
    #     selected_choice = question.choice_set.get(pk=request.POST["choice"])
    # except (KeyError, Choice.DoesNotExist):
    #     # Redisplay the question voting form.
    #     return render(
    #         request,
    #         "polls/detail.html",
    #         {
    #             "question": question,
    #             "error_message": "You didn't select a choice.",
    #         },
    #     )
    # else:
    #     selected_choice.votes += 1
    #     selected_choice.save()
    #     # Always return an HttpResponseRedirect after successfully dealing
    #     # with POST data. This prevents data from being posted twice if a
    #     # user hits the Back button.
    #     return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
