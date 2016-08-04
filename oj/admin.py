from django.contrib import admin

from .models import Problem, User, Submission, Waiting

admin.site.register(Problem)
admin.site.register(User)
admin.site.register(Submission)
admin.site.register(Waiting)
