from django.contrib import admin
from .models import RawProblem, CleanProblem, TakenProblems

admin.site.register(RawProblem)
admin.site.register(CleanProblem)
admin.site.register(TakenProblems)