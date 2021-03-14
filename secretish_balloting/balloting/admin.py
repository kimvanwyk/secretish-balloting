from django.contrib import admin

from .models import Choice, Question, Ballot, Voter


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2


class BallotAdmin(admin.ModelAdmin):
    list_display = (
        "name_text",
        "url_fragment_text",
        "opening_date",
        "closing_date",
        "is_open",
    )
    fieldsets = [
        (None, {"fields": ["name_text", "url_fragment_text"]}),
        (
            "Date information",
            {"fields": ["opening_date", "closing_date"]},
        ),
    ]


class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]


class VoterAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["ballot", "email_text", "description_text"]}),
    ]


admin.site.register(Ballot, BallotAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Voter, VoterAdmin)
