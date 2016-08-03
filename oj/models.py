from django.db import models

class Problem(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.title

class Submission(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    source = models.TextField()

    def __str__(self):
        return self.source
