from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

import member
import stock
from stock import views

app_name ="stock"

urlpatterns = [
    path('company/', stock.views.CompanyList.as_view(), name='company_list2'), #메인 = 회사영역
    path('detail/<str:a>', stock.views.detail, name='company_detail'), #회사정보 디테일
    path('companyFilter/', stock.views.filter, name='company_filter'), #회사검색
    path('stockdetail/<str:s>', stock.views.stock_detail, name="stock_detail"),
    path('companyUpdate/', stock.views.update, name='stock_update'), #업데이트와 딜리트는, 타입과 프라이머리 키를 조건으로 넘겨서 처리
    # path('mypage/', member.views.select, name='my_page'),
]
