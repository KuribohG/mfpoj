from django.contrib import admin

from .models import Problem, Submission, Waiting

admin.site.register(Problem)
admin.site.register(Submission)
admin.site.register(Waiting)
