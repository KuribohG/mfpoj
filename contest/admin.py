from django.contrib import admin

from .models import Contest, ContestProblem, ContestSubmission, ContestUser

admin.site.register(Contest)
admin.site.register(ContestProblem)
admin.site.register(ContestUser)
admin.site.register(ContestSubmission)
