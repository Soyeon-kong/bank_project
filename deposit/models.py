from django.db import models
from member.models import Member

# Create your models here.
class Deposit(models.Model):
    deposit_id = models.IntegerField(primary_key=True)
    bank = models.CharField(max_length=100)  #은행명
    product = models.CharField(max_length=100) #상품명
    rate_6 = models.CharField(max_length=100, default="-") #6개월 이자율
    rate_12 = models.CharField(max_length=100, default="-") #12개월 이자율
    rate_24 = models.CharField(max_length=100, default="-") #24개월 이자율
    rate_36 = models.CharField(max_length=100, default="-") #36개월 이자율
    rate_type = models.CharField(max_length=100, default="") #이자 계산방식
    join_way = models.CharField(max_length=100, default="") #가입방법
    mtrt_int = models.TextField(default="") #만기 후 이자율
    spcl_cnd = models.TextField(default="") #우대조건
    join_member = models.CharField(max_length=100, default="") #가입대상
    etc_note = models.TextField(default="") #유의사항
    max_limit = models.TextField(default="") #최고한도

class Mydepositlist(models.Model):
    member_id = models.ForeignKey(Member, on_delete=models.CASCADE)
    # member_id = models.CharField(max_length=100)
    product_name = models.CharField(max_length=100)