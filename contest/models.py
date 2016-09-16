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
    score = models.IntegerField(default=0)
    
    def stat_default():
        return {"Accepted": 0, 
                "Presentation Error": 0, 
                "Time Limit Exceeded": 0, 
                "Memory Limit Exceeded": 0, 
                "Wrong Answer": 0, 
                "Runtime Error": 0, 
                "Output Limit Exceeded": 0, 
                "Compile Error": 0, 
                "System Error": 0, 
               }
    stat = models.TextField(default=stat_default())

    def __str__(self):
        return self.contest.title + self.user.username
    
class ContestProblem(models.Model):
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    number = models.CharField(max_length=10)
    ac = models.IntegerField(default=0)
    submit = models.IntegerField(default=0)

    def __str__(self):
        return self.contest.title + self.problem.title

class ContestSubmission(Submission):
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    contest_problem = models.ForeignKey(ContestProblem, on_delete=models.CASCADE)
    contest_user = models.ForeignKey(ContestUser, on_delete=models.CASCADE)
