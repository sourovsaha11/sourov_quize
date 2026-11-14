from django.contrib import admin
from .models import Quiz, Question, Option, Participant, Result

# Register your models here.

class OptionInline(admin.TabularInline):
    model = Option
    extra = 4


class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question', 'quiz']
    inlines = [OptionInline]


admin.site.register(Quiz)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Option)
admin.site.register(Participant)
admin.site.register(Result)
