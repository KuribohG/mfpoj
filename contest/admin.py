from django.contrib import admin

from .models import Contest, ContestProblem, ContestSubmission

admin.site.register(Contest)
admin.site.register(ContestProblem)
admin.site.register(ContestSubmission)
