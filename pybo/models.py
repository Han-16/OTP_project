from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    author = models.ForeignKey(User, on_delete = models.CASCADE, related_name='author_question')
    subject = models.CharField(max_length = 200)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    modify_count = models.IntegerField(default=0)
    question_hash = models.CharField(max_length = 200)
    qr_code = models.ImageField(upload_to='static/qrcodes/', blank=True)

    STATUS_CHOICES = [
        ('pending', '대기'),  # 결재 대기
        ('approved', '허가'),  # 결재 허가
        ('rejected', '반려'),  # 결재 반려
        ('holding', '보류'),  # 결재 보류
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return self.subject

class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'author_answer')
    question = models.ForeignKey(Question, on_delete = models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    modify_count = models.IntegerField(default=0)

    def __str__(self):
        return self.content

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auth_comment")
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null = True, blank = True)
    question = models.ForeignKey(Question, null = True, blank = True, on_delete = models.CASCADE)
    answer = models.ForeignKey(Answer, null = True, blank = True, on_delete = models.CASCADE)
    modify_count = models.IntegerField(default=0)

    def __str__(self):
        return self.content