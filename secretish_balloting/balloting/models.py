import datetime

from django.db import models
from django.utils import timezone


class Ballot(models.Model):
    name_text = models.CharField(max_length=100)
    opening_date = models.DateTimeField("opening date and time")
    closing_date = models.DateTimeField("closing date and time")
    url_fragment_text = models.CharField(
        max_length=40, help_text="Slug text to be used in the urls for this ballot"
    )

    def __str__(self):
        return self.name_text

    def is_open(self):
        return self.opening_date <= timezone.now() <= self.closing_date

    is_open.admin_order_field = "opening_date"
    is_open.boolean = True
    is_open.short_description = "Ballot open?"


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
