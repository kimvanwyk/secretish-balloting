from django.contrib import admin

from .models import Choice, Question, Ballot


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2


class BallotAdmin(admin.ModelAdmin):
    list_display = ("name_text", "opening_date", "closing_date", "is_open")
    fieldsets = [
        (None, {"fields": ["name_text"]}),
        (
            "Date information",
            {"fields": ["opening_date", "closing_date"], "classes": ["collapse"]},
        ),
    ]


class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]


admin.site.register(Ballot, BallotAdmin)
admin.site.register(Question, QuestionAdmin)
