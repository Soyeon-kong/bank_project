from django.db import models


# Create your models here.
class Member(models.Model):
    # 파이썬의 변수 ,DB 테이블의 항목
    id = models.CharField(max_length=100, primary_key=True)
    pw = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    tel = models.CharField(max_length=100)
    stock_list = models.CharField(max_length=100)
    deposit_list = models.CharField(max_length=100)

    def __str__(self):
        return '아이디 : ' + self.id + '패스워드 : ' + self.pw + '이름 : ' + self.name + \
               self.stock_list + self.deposit_list + self.tel