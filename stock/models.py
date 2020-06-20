from django.db import models

# Create your models here.

class Stock(models.Model):
    stock_name = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now=True)
    high_price = models.CharField(max_length=100, default='')
    low_price = models.CharField(max_length=100, default='')
    now_price = models.CharField(max_length=100, default='')

    def __str__(self):
        return '상품 ID : ' + str(self.id) + ' ' + \
               '주식상품명 : ' + self.stock_name + ' ' + \
               '기준 날짜 : ' + self.date + ' ' \
               '고가 : ' + str(self.high_price) + ' ' + \
               '저가 : ' + self.low_price + ' ' + \
               '현재가 : ' + self.now_price + ' '

class Company(models.Model):
    company_name = models.CharField(max_length=100)
    company_code = models.CharField(max_length=100)
    company_page = models.CharField(max_length=350)

    def __str__(self):
        return '회사 ID : ' + str(self.id) + ' ' + \
               '회사이름 : ' + str(self.company_name) + ' ' + \
               '종목코드 : ' + str(self.company_code) + ' ' + \
               '홈페이지 : ' + str(self.company_page)


class TTT(models.Model):
    company_name = models.CharField(max_length=100)
    company_code = models.CharField(max_length=100)
    company_page = models.CharField(max_length=350)

    def __str__(self):
        return '회사 ID : ' + str(self.id) + ' ' + \
               '회사이름 : ' + str(self.company_name) + ' ' + \
               '종목코드 : ' + str(self.company_code) + ' ' + \
               '홈페이지 : ' + str(self.company_page)
