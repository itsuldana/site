from django.db import models


class QuizQuestion(models.Model):
    text = models.CharField(max_length=255)
    tags = models.ManyToManyField('webapp.Tag')


class QuizOption(models.Model):
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=255)
    tag = models.ForeignKey('webapp.Tag', on_delete=models.CASCADE)  # связанный тег
