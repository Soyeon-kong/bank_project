from django.urls import path
from board.views import *


urlpatterns=[
    path('list/',BoardList.as_view(),name='boardlist'),
    path('add/',BoardCreate.as_view(),name='boardcreate'),
    path('detail/<int:pk>',BoardDetail.as_view(),name='boarddetail'),
    path('update/<int:pk>',BoardUpdate.as_view(),name='boardupdate'),
    path('delete/',deleteboard,name='boarddelete')
]