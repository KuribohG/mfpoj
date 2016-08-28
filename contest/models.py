from django.db import models

from oj.models import Problem, Submission, User

class Contest(models.Model):
    title = models.CharField(max_length=100)
    start = models.DateTimeField()
    end = models.DateTimeField()
    
    def __str__(self):
        return self.title

class ContestUser(models.Model):
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.contest.title + self.user.username
    
class ContestProblem(models.Model):
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    number = models.CharField(max_length=10)

    def __str__(self):
        return self.contest.title + self.problem.title

class ContestSubmission(Submission):
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    contest_problem = models.ForeignKey(ContestProblem, on_delete=models.CASCADE)
    contest_user = models.ForeignKey(ContestUser, on_delete=models.CASCADE)
