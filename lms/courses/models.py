from random import shuffle
from django.db import models
from accounts.models import User, Instructor


class Course(models.Model):

    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    what_to_learn = models.TextField(max_length=1000)
    thumbnail = models.ImageField(
        upload_to='course_thumbnails/', null=False, blank=False)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    # duration = models.PositiveIntegerField(help_text='Duration in hours')
    # certificate = models.FileField(upload_to='course_certificate/', blank=False, null=False)
    upload_date = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=100)
    instructor = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Course_Videos(models.Model):
    title = models.CharField(max_length=100)
    video = models.FileField(upload_to='course_video/',
                             blank=False, null=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)


class Quiz(models.Model):
    title = models.CharField(max_length=200)

    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="course")

    def __str__(self):
        return self.title


class QuizQuestion(models.Model):
    quiz = models.ForeignKey(
        Quiz, on_delete=models.CASCADE, related_name="quiz")
    question = models.TextField()
    marks = models.PositiveIntegerField(default=1)

    def __str__(self) -> str:
        return self.question

    def get_answers(self):
        answer_objs = list(QuizMCQOption.objects.filter(question=self))
        data = []
        shuffle(answer_objs)
        for answer_obj in answer_objs:
            data.append({
                'id': answer_obj.id,
                'answer': answer_obj.option,
                'is_correct': answer_obj.is_correct
            })
        return data


class QuizMCQOption(models.Model):
    question = models.ForeignKey(
        QuizQuestion, on_delete=models.CASCADE, related_name="MCQAnswer")
    option = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.option


class QuizResultModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # course = models.ForeignKey(Course,on_delete=models.CASCADE)
    course = models.CharField(max_length=255)
    score = models.IntegerField()
    is_completed = models.BooleanField(default=False)
    date_submitted = models.DateTimeField(auto_now_add=True)
