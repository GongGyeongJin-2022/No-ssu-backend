from datetime import datetime
from django.db import models
from accounts.models import User


class Marker(models.Model):
    longitude = models.DecimalField(max_digits=20, decimal_places=10)   # 위도
    latitude = models.DecimalField(max_digits=20, decimal_places=10)    # 경도 
    image = models.ImageField(blank=True, null=True, upload_to='images/')   # 사진
    explanation = models.TextField()      # 설명
    tags = models.ManyToManyField('Tag', blank=True)    # 태그 (쓰레기 종류)
    reward = models.ForeignKey('Reward', on_delete=models.CASCADE)  # 현상금
    posted_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posted_user')  # 올린 사람
    cleanup_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='cleanup_user')    # 치운 사람
    posted_time = models.DateTimeField(auto_now_add=True)  # 올린 시간

    def __str__(self):
        return self.image


class Tag(models.Model):
    name = models.CharField(max_length=20) 

    def __str__(self):
        return self.name


class Reward(models.Model):
    reward = models.IntegerField(default=0)  # 현상금
    gave_user = models.CharField(max_length=20)      # 준 사람
    received_user = models.CharField(max_length=20)  # 받은 사람
    date = models.DateTimeField(auto_now_add=True)   # 현상금 지급 시간

    def __str__(self):
        return self.received_user
