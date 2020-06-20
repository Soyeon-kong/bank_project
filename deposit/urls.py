from django.urls import path

import deposit.views

app_name = 'deposit'

urlpatterns = [
    path('', deposit.views.search, name="search"),
    path('search/', deposit.views.search_result, name="search_result"),
    path('mydeposit/', deposit.views.my_deposit, name="my_deposit"),
    path('mydeposit/list',deposit.views.my_deposit_list, name="my_deposit_list"),
    path('detail/<d_name>',deposit.views.detail, name="detail"),
    path('delete/', deposit.views.delete, name="delete"),
]

