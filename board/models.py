from django import forms
from django.db import models

# Create your models here.


class Board(models.Model):
    #파이썬의 변수 ,DB 테이블의 항목
    b_number = models.AutoField(primary_key=True)
    b_title = models.CharField(max_length=100)
    b_content = models.TextField(default="")
    #사진 이미지 업로드시
    b_photo = models.ImageField(upload_to='photos/%Y/%m/%d', default='photos/no_image.png')
    b_hit =models.IntegerField(default=0)
    #게시글 작성 날짜
    b_date =models.DateTimeField(auto_now_add= True)
    b_writer = models.CharField(max_length=100)

    @property
    def hit_up(self):
        self.b_hit += 1
        self.save()
class UpdateForm(forms.ModelForm):
    class Meta:
        model = Board
        exclude = ['b_hit','b_writer']
