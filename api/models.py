
from uuid import uuid4

from django.db import models
from accounts.models import User
from django.utils import timezone


def date_upload_to(instance, filename):
    # upload_to="%Y/%m/%d" 처럼 날짜로 세분화
    ymd_path = timezone.now().strftime('%Y/%m/%d')
    # 길이 32 인 uuid 값
    uuid_name = uuid4().hex
    # 확장자 추출
    extension = '.jpeg'
    # 결합 후 return
    return '/'.join([
        'images',
        ymd_path,
        uuid_name + extension,
        ])

class Marker(models.Model):
    """
    마커 테이블
    longitude : 위도
    latitude : 경도
    image : 사진
    explanation : 설명
    tags : 태그(쓰레기 종류)
    size : 크기(쓰레기 사이즈)
    reward : 현산금
    posted_user : 게시자
    cleanup_user : 처리자
    posted_time : 게시 시간
    status : 상태(처리 부탁, 처리 확인 중, 처리 완료)
    """

    SIZE_CHOICES = (
        ('S', 'SMALL'),
        ('M', 'MEDIUM'),
        ('L', 'LARGE'),
    )

    STATUS_CHOICES = (
        ('U', 'uncleaned_marker'),
        ('W', 'waiting_marker'),
        ('C', 'cleanup_marker'),
    )

    longitude = models.DecimalField(max_digits=20, decimal_places=14)  # 위도
    latitude = models.DecimalField(max_digits=20, decimal_places=14)  # 경도
    image = models.FileField(blank=True, null=True, upload_to=date_upload_to, max_length=300)  # 사진
    explanation = models.TextField(default="")
    tags = models.ManyToManyField('Tag')
    size = models.CharField(max_length=1, choices=SIZE_CHOICES)
    reward = models.ForeignKey('Reward', on_delete=models.CASCADE, null=False)
    posted_user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name='posted_user')
    cleanup_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='cleanup_user')
    posted_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='W')

    def __str__(self):
        return self.image


class Tag(models.Model):
    """
    태그 테이블
    name : 태그 명
    """
    name = models.CharField(max_length=20) 

    def __str__(self):
        return self.name


class Size(models.Model):
    """
    사이즈 테이블
    name : 사이즈 명
    """
    size = models.CharField(max_length=10) 

    def __str__(self):
        return self.size       


class Reward(models.Model):
    """
    리워드 테이블
    reward : 현상금
    gave_user : 준 사람
    received_user : 받은 사람
    date : 지급 시간
    """

    reward = models.IntegerField(default=0)  # 현상금
    gave_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True,blank=True, related_name='gave_user')
    received_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='received_user')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.received_user.__str__()