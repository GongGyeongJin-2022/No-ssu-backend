from django.db import models

class Marker(models.Model):
    longitude = models.DecimalField(max_digits=20, decimal_places=10)  # 위도
    latitude = models.DecimalField(max_digits=20, decimal_places=10)   # 경도 
    image = models.ImageField(blank=True,null=True,upload_to='images/')      # 사진
    explanation = models.TextField() # 설명

    def __str__(self):
        return self.image
