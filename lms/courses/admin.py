from django.contrib import admin
from .models import *

# Register your models here.
# admin.site.register(Course)
# admin.site.register(Course_Videos)
# admin.site.register(Quiz)
# admin.site.register(QuizQuestion)
# admin.site.register(QuizMCQOption)



class MCQOptionAdmin(admin.StackedInline):
    model = QuizMCQOption

class QuestionAdmin(admin.ModelAdmin):
    inlines = [MCQOptionAdmin]


admin.site.register(Course)
admin.site.register(Quiz)
admin.site.register(QuizQuestion , QuestionAdmin)
admin.site.register(QuizMCQOption )