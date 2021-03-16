import datetime
import random

from django.db import models, transaction, IntegrityError
from django.utils import timezone
from django.utils.crypto import get_random_string


class Ballot(models.Model):
    name_text = models.CharField(max_length=100)
    opening_date = models.DateTimeField("opening date and time")
    closing_date = models.DateTimeField("closing date and time")
    url_fragment_text = models.CharField(
        max_length=40, help_text="Slug text to be used in the urls for this ballot"
    )
    url_summary_fragment_text = models.CharField(
        max_length=40,
        help_text="Slug text to be used in the summary url for this ballot",
    )

    def __str__(self):
        return self.name_text

    def is_open(self):
        return self.opening_date <= timezone.now() <= self.closing_date

    is_open.admin_order_field = "opening_date"
    is_open.boolean = True
    is_open.short_description = "Ballot open?"

    def save(self, *args, **kwds):
        if self.url_summary_fragment_text is None:
            self.url_summary_fragment_text = random.randint(10000000, 99999999)
        super().save(*args, **kwds)


class Question(models.Model):
    ballot = models.ForeignKey(Ballot, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=100)
    order_int = models.IntegerField("Question order")

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=100)

    def __str__(self):
        return self.choice_text


class Voter(models.Model):
    ballot = models.ForeignKey(Ballot, on_delete=models.CASCADE)
    email_text = models.EmailField("Email address")
    description_text = models.CharField(
        "Description", max_length=200, help_text="A descriptive note for this voter"
    )
    emailed_bool = models.BooleanField(
        "Voter has been emailed voting instructions", default=False
    )
    url_fragment_text = models.CharField(
        max_length=20, unique=True, null=True, blank=True, default=None
    )

    def __str__(self):
        return self.description_text

    def save(self, *args, **kwds):
        if self.url_fragment_text is None:
            # get current url fragments to ensure a unique one
            fragments = [o.url_fragment_text for o in Voter.objects.all()]
            while True:
                self.url_fragment_text = random.randint(10000000, 99999999)
                if self.url_fragment_text not in fragments:
                    break
        super().save(*args, **kwds)


class Vote(models.Model):
    voter = models.ForeignKey(Voter, on_delete=models.CASCADE)
    choice = models.ForeignKey(
        Choice, null=True, default=None, on_delete=models.CASCADE
    )
